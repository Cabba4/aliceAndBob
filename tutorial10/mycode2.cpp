#include "openfhe.h"
#include <random>
using namespace lbcrypto;

int main() {
    // Step 1: Set CryptoContext
    CCParams<CryptoContextBFVRNS> parameters;
    parameters.SetPlaintextModulus(65537);
    parameters.SetMultiplicativeDepth(2);
    CryptoContext<DCRTPoly> cryptoContext = GenCryptoContext(parameters);

    // Enable features that you wish to use
    cryptoContext->Enable(PKE);
    cryptoContext->Enable(KEYSWITCH);
    cryptoContext->Enable(LEVELEDSHE);

    // Step 2: Key Generation
    // Initialize Public Key Containers
    KeyPair<DCRTPoly> keyPair;
    // Generate a public/private key pair
    keyPair = cryptoContext->KeyGen();
    // Generate the relinearization key
    cryptoContext->EvalMultKeyGen(keyPair.secretKey);

    // Step 3: Encryption
    // First plaintext vector is encoded

    std::vector<std::vector<int64_t>> vectors;
    std::default_random_engine generator;
    std::uniform_int_distribution<int64_t> distribution(1,10);

    // Generate 10 vectors, each with 5 random integers
    for (int i = 0; i < 10; ++i) {
        std::vector<int64_t> tempVector(5);
        for (int j = 0; j < 5; ++j) {
            tempVector[j] = distribution(generator);
        }
        vectors.push_back(tempVector);

        // Print the generated vector
        std::cout << "Vector " << i + 1 << ": ";
        for (auto val : tempVector) {
            std::cout << val << " ";
        }
        std::cout << std::endl;
    }

    std::vector<Ciphertext<DCRTPoly>> ciphertexts;

    for (const auto& vec : vectors) {
        Plaintext plaintext = cryptoContext->MakePackedPlaintext(vec);
        ciphertexts.push_back(cryptoContext->Encrypt(keyPair.publicKey, plaintext));
    }

    auto aggregatedCiphertext = ciphertexts[0];
    for (size_t i = 1; i < ciphertexts.size(); ++i) {
        aggregatedCiphertext = cryptoContext->EvalAdd(aggregatedCiphertext, ciphertexts[i]);
    }

    Plaintext plaintextAggregateResult;
    cryptoContext->Decrypt(keyPair.secretKey, aggregatedCiphertext, &plaintextAggregateResult);
    std::cout << "Aggregated result: " << plaintextAggregateResult << std::endl;


    // std::vector<int64_t> vectorOfInts1 = {1, 2, 3, 4, 5};
    // Plaintext plaintext1 = cryptoContext->MakePackedPlaintext(vectorOfInts1);
    // Second plaintext vector is encoded
    // std::vector<int64_t> vectorOfInts2 = {3, 2, 1, 4, 5};
    // Plaintext plaintext2 = cryptoContext->MakePackedPlaintext(vectorOfInts2);
    // The encoded vectors are encrypted
    // auto ciphertext1 = cryptoContext->Encrypt(keyPair.publicKey, plaintext1);
    // auto ciphertext2 = cryptoContext->Encrypt(keyPair.publicKey, plaintext2);

    // Step 4: Evaluation
    // Homomorphic additions
    // auto ciphertextAddResult = cryptoContext->EvalAdd(ciphertext1, ciphertext2);

    // Step 5: Decryption
    // Decrypt the result of additions
    // Plaintext plaintextAddResult;
    // cryptoContext->Decrypt(keyPair.secretKey, ciphertextAddResult,&plaintextAddResult);
    // std::cout << "Plaintext #1: " << plaintext1 << std::endl;
    // std::cout << "Plaintext #2: " << plaintext2 << std::endl;
    
    // // Output results
    // std::cout << "\nResults of homomorphic computations" << std::endl;
    // std::cout << "#1 + #2: " << plaintextAddResult << std::endl;
    return 0;
}