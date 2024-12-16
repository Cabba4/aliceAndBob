from mnist import MNIST
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from openfhe import *
import random

## export PYTHONPATH=/usr/local:$PYTHONPATH


# Preprocessing functions
def resize_images(images):
    resized_images = []
    for image in images:
        image_14x14 = image.reshape(14, 2, 14, 2).mean(axis=(1, 3))
        resized_images.append(image_14x14)
    return np.array(resized_images)

def preprocess_data(images, labels):
    filtered_images, filtered_labels = [], []
    ## Positive class 1 if image is 3
    for i in range(len(labels)):
        if labels[i] == 3:
            filtered_images.append(images[i])
            filtered_labels.append(1)
    ## Negative class 0 if image is 8
        elif labels[i] == 8:
            filtered_images.append(images[i])
            filtered_labels.append(0)

    filtered_images = np.array(filtered_images)
    filtered_labels = np.array(filtered_labels)
    resized_images = resize_images(filtered_images).astype('float32') / 255.0
    resized_images = resized_images.reshape((resized_images.shape[0], -1))
    return resized_images, filtered_labels

# Logistic Regression functions
def train_model(train_images, train_labels):
    model = LogisticRegression(max_iter=1000)
    model.fit(train_images, train_labels)
    return model

def test_model(model, test_images, test_labels):
    test_predictions = model.predict(test_images)
    test_accuracy = accuracy_score(test_labels, test_predictions)
    print(f"Test Accuracy: {test_accuracy * 100:.2f}%")
    return test_accuracy

def HE(weights, bias, test_image):
    # Step 1: Initialize the CKKS context
    mult_depth, scale_mod_size, batch_size = 5, 41, 1024    # Values found by trial and error for scale_mod_size.

    parameters = CCParamsCKKSRNS()
    parameters.SetMultiplicativeDepth(mult_depth)
    parameters.SetScalingModSize(scale_mod_size)
    parameters.SetBatchSize(batch_size)

    cc = GenCryptoContext(parameters)
    cc.Enable(PKESchemeFeature.PKE)
    cc.Enable(PKESchemeFeature.KEYSWITCH)
    cc.Enable(PKESchemeFeature.LEVELEDSHE)
    cc.Enable(PKESchemeFeature.ADVANCEDSHE)

    print(f"The CKKS scheme is using ring dimension: {cc.GetRingDimension()}")

    # Generate keys
    keys= cc.KeyGen()
    cc.EvalMultKeyGen(keys.secretKey)
    cc.EvalSumKeyGen(keys.secretKey)
    cc.EvalRotateKeyGen(keys.secretKey, [1, -2])

    # Step 2: Encrypt weights, bias, and test image
    encrypted_weights = cc.Encrypt(keys.publicKey, cc.MakeCKKSPackedPlaintext(weights))
    encrypted_bias = cc.Encrypt(keys.publicKey, cc.MakeCKKSPackedPlaintext([bias]))
    encrypted_image = cc.Encrypt(keys.publicKey, cc.MakeCKKSPackedPlaintext(test_image))

    # Step 3: Perform inference on encrypted data
    encrypted_prediction = homomorphic_logistic_regression_predict(encrypted_weights, encrypted_image, encrypted_bias, cc, test_image)

    # Step 4: Decrypt prediction for verification
    decrypted_prediction = cc.Decrypt(encrypted_prediction, keys.secretKey)
    decrypted_prediction.SetLength(1)  # Only one value
    print("Decrypted prediction:", decrypted_prediction)
    prediction_value = decrypted_prediction.GetRealPackedValue()[0]
    
        # Now classify based on the value
    if prediction_value > 1:
        predicted_class = 0  # Positive class
    else:
        predicted_class = 1  # Negative class

    # Output the results
    print(f"Decrypted Prediction: {prediction_value}")
    print(f"Predicted Class: {predicted_class}")

    return predicted_class


# Logistic regression model algorithm
def homomorphic_logistic_regression_predict(encrypted_weights, encrypted_image, encrypted_bias, cc, test_image):
    # Compute dot product of encrypted image and encrypted weights (vectorized approach)
    encrypted_dot_product = cc.EvalInnerProduct(encrypted_weights, encrypted_image, 512)

    # Add the bias term to the dot product
    encrypted_sum_with_bias = cc.EvalAdd(encrypted_dot_product, encrypted_bias)

    # Apply the polynomial approximation for sigmoid: y = 0.5 - 0.25 * x - 0.0417 * x^3
    x = encrypted_sum_with_bias
    x2 = cc.EvalMult(x, x)  # x^2
    x3 = cc.EvalMult(x2, x)  # x^3

    # Apply the terms in the sigmoid approximation polynomial
    term1 = cc.EvalMult(x3, cc.MakeCKKSPackedPlaintext([-0.0417]))  # 0.-0.0417 * x^3
    term2 = cc.EvalMult(x, cc.MakeCKKSPackedPlaintext([0.25]))   # 0.25 * x
    constant_term = cc.MakeCKKSPackedPlaintext([0.5])  # Constant term 0.5

    sum_1 = cc.EvalAdd(term2, term1)
    sigmoid = cc.EvalAdd(sum_1, 0.5)

    return sigmoid


## Tried to implement algo 5
# def homomorphic_logistic_regression_predict(encrypted_weights, encrypted_image, encrypted_bias, cc, wBits, pBits, g, f):
#     # Initialize necessary ciphertexts
#     encM = None  # For the weighted sum of features
#     encM_prime = None
#     encM_sum = None
#     encG = None  # For gradients or similar intermediate values
#     encC = None  # Intermediate results
#     encZ = None  # Another intermediate result
#     encW_final = None
#     encV_final = None

#     # Loop for 0 ≤ j < f / g (assuming f / g is your feature count divided by the grouping size)
#     for j in range(f // g):
#         # Step 2: rescale(multiply(encZj, encVj), wBits)
#         encM = cc.Rescale(cc.EvalMult(encrypted_image, encrypted_weights), wBits)
        
#         # Step 3: encM = encSumColVec(encM, pBits)
#         encM_sum = cc.EvalAdd(encM, cc.MakeCKKSPackedPlaintext([-100]))  # Example offset
#         encM_sum = cc.Rescale(encM_sum, pBits)

#         # Step 4: Compute the sum of previous terms for encM
#         for k in range(f // g):
#             encM = cc.EvalAdd(encM, encM_sum)

#         # Steps 5-8 for encWj and encVj (update encrypted weights and values)
#         encW_prime = cc.Rescale(cc.EvalMult(encrypted_weights, encM), wBits)
#         encG = cc.Rescale(cc.EvalMult(encM, encW_prime), pBits)

#         # Step 10: Compute encZ with scaling factor gamma
#         encZ = cc.EvalMult(encrypted_image, cc.MakeCKKSPackedPlaintext([0.5]))  # Using a simple gamma for demonstration
        
#         # Step 11: Apply the modDownTo operation to reduce precision
#         encZ = cc.ModDownTo(encZ, encM)
        
#         # Step 12: Compute encC (step 15 and 16 with encG and encWj adjustments)
#         encC = cc.EvalAdd(encZ, encG)
        
#         # Step 13: Adjust encrypted weights and bias using EvalMult and EvalAdd as needed
#         encW_prime_new = cc.EvalMult(encW_prime, cc.MakeCKKSPackedPlaintext([1 - 0.1]))  # Example update
#         encC = cc.EvalAdd(encC, encW_prime_new)

#         # Final steps to finalize encWj+ and encVj+ (using modulation)
#         encW_final = cc.EvalMult(encW_prime_new, cc.MakeCKKSPackedPlaintext([1]))  # Example update step
#         encV_final = cc.EvalAdd(encW_final, encC)
        
#         # Perform modDownTo on the final results
#         encV_final = cc.ModDownTo(encV_final, encrypted_bias)  # Using bias for final scaling
#         encW_final = cc.ModDownTo(encW_final, encrypted_weights)

#     # Return the final encrypted ciphertexts encWj+ and encVj+
#     return encW_final, encV_final


# Main function
def main():
    # Load MNIST data
    mndata = MNIST('samples')
    images, labels = mndata.load_training()

    # Preprocess and split data
    train_images, train_labels = preprocess_data(images, labels)
    train_images, val_images, train_labels, val_labels = train_test_split(
        train_images, train_labels, test_size=0.165, random_state=42
    )

    # Train model
    model = train_model(train_images, train_labels)

    # Validate the model
    val_predictions = model.predict(val_images)
    val_accuracy = accuracy_score(val_labels, val_predictions)
    val_precision = precision_score(val_labels, val_predictions)
    val_recall = recall_score(val_labels, val_predictions)
    val_f1 = f1_score(val_labels, val_predictions)

    print(f"Validation Metrics:")
    print(f"- Accuracy: {val_accuracy * 100:.2f}%")
    print(f"- Precision: {val_precision:.2f}")
    print(f"- Recall: {val_recall:.2f}")
    print(f"- F1 Score: {val_f1:.2f}")

    # Preprocess and test the model
    test_images, test_labels = mndata.load_testing()
    test_resized_images, test_filtered_labels = preprocess_data(test_images, test_labels)

    print("\nTesting the Model on the Test Dataset...")
    test_accuracy = test_model(model, test_resized_images, test_filtered_labels)

    weights, bias = model.coef_.flatten(), model.intercept_[0]

    # # Encrypt and test one image
    print("Running homomorphic encryption on one test image...")
    index = random.randrange(0,len(test_resized_images))
    print("Real Class of test image is: ", test_filtered_labels[index])
    ## If label = 1 then image is 3 and 8 if label = 0

    prediction = HE(weights, bias, test_resized_images[index])

    if prediction == 1:
        print("Model predicts it is : 3")
    else:
        print("Model predicts it is : 8")
    
    # Initialize a counter for correct predictions
    correct_predictions = 0

    # Loop through all test images
    for i in range(30):
        # Get the true label (1 for 3, 0 for 8)
        true_label = test_filtered_labels[i]
        if true_label == 1:
            true_label_str = "3"
        else:
            true_label_str = "8"
        
        # Run homomorphic encryption prediction for the current image
        prediction = HE(weights, bias, test_resized_images[i])
        
        # Print prediction
        if prediction == 1:
            predicted_class = "3"
        else:
            predicted_class = "8"

        # Print the result for the current test image
        print(f"True label: {true_label_str}, Model predicts: {predicted_class}")

        # Compare prediction with true label
        if prediction == true_label:
            correct_predictions += 1

    # Print the total number of correct predictions
    print(f"Correct predictions: {correct_predictions} out of 30")


if __name__ == "__main__":
    main()
