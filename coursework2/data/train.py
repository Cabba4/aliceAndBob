import numpy as np

# Sigmoid function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Logistic regression function
def logistic_regression(X, y, lr=0.01, epochs=10):
    # Initialize weights and bias
    weights = np.zeros(X.shape[1])
    bias = 0
    
    # Training loop
    for epoch in range(epochs):
        # Linear combination
        z = np.dot(X, weights) + bias
        
        # Sigmoid activation
        predictions = sigmoid(z)
        
        # Calculate the loss (binary cross-entropy)
        loss = -np.mean(y * np.log(predictions) + (1 - y) * np.log(1 - predictions))
        
        # Gradients
        dw = np.dot(X.T, (predictions - y)) / X.shape[0]
        db = np.mean(predictions - y)
        
        # Update weights and bias
        weights -= lr * dw
        bias -= lr * db
        
        if epoch % 100 == 0:
            print(f"Epoch {epoch}, Loss: {loss}")
    
    return weights, bias
