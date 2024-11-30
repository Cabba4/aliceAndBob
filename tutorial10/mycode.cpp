#include "openfhe.h"
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
    std::vector<int64_t> vectorOfInts1 = {1, 2, 3, 4, 5};
    Plaintext plaintext1 = cryptoContext->MakePackedPlaintext(vectorOfInts1);
    // Second plaintext vector is encoded
    std::vector<int64_t> vectorOfInts2 = {3, 2, 1, 4, 5};
    Plaintext plaintext2 = cryptoContext->MakePackedPlaintext(vectorOfInts2);
    // The encoded vectors are encrypted
    auto ciphertext1 = cryptoContext->Encrypt(keyPair.publicKey, plaintext1);
    auto ciphertext2 = cryptoContext->Encrypt(keyPair.publicKey, plaintext2);

    // Step 4: Evaluation
    // Homomorphic additions
    auto ciphertextAddResult = cryptoContext->EvalAdd(ciphertext1, ciphertext2);

    // Step 5: Decryption
    // Decrypt the result of additions
    Plaintext plaintextAddResult;
    cryptoContext->Decrypt(keyPair.secretKey, ciphertextAddResult,&plaintextAddResult);
    std::cout << "Plaintext #1: " << plaintext1 << std::endl;
    std::cout << "Plaintext #2: " << plaintext2 << std::endl;
    
    // Output results
    std::cout << "\nResults of homomorphic computations" << std::endl;
    std::cout << "#1 + #2: " << plaintextAddResult << std::endl;
    return 0;
}