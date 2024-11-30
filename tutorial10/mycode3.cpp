#include "openfhe.h"
#include <random>
#include <fstream>
#include <chrono>
using namespace lbcrypto;

int main() {
    using Clock = std::chrono::high_resolution_clock;

    // Step 1: Set CryptoContext
    CCParams<CryptoContextBFVRNS> parameters;
    parameters.SetPlaintextModulus(65537);
    parameters.SetMultiplicativeDepth(2);
    CryptoContext<DCRTPoly> cryptoContext = GenCryptoContext(parameters);

    cryptoContext->Enable(PKE);
    cryptoContext->Enable(KEYSWITCH);
    cryptoContext->Enable(LEVELEDSHE);

    // Measure key generation time
    auto start = Clock::now();
    KeyPair<DCRTPoly> keyPair = cryptoContext->KeyGen();
    cryptoContext->EvalMultKeyGen(keyPair.secretKey);
    auto end = Clock::now();
    std::cout << "Key Generation Time: "
              << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() << " ms\n";

    // Save keys to files
    std::ofstream publicKeyFile("public_key.txt");
    publicKeyFile << keyPair.publicKey;
    publicKeyFile.close();

    std::ofstream secretKeyFile("secret_key.txt");
    secretKeyFile << keyPair.secretKey;
    secretKeyFile.close();

    std::ofstream evalKeyFile("eval_key.txt");
    cryptoContext->SerializeEvalMultKey(evalKeyFile, SerType::BINARY);
    evalKeyFile.close();

    // Measure key sizes
    std::ifstream pkFile("public_key.txt", std::ios::binary | std::ios::ate);
    std::ifstream skFile("secret_key.txt", std::ios::binary | std::ios::ate);
    std::ifstream ekFile("eval_key.txt", std::ios::binary | std::ios::ate);

    auto pkSize = pkFile.tellg();
    auto skSize = skFile.tellg();
    auto ekSize = ekFile.tellg();

    pkFile.close();
    skFile.close();
    ekFile.close();

    std::cout << "Public Key Size: " << pkSize << " bytes\n";
    std::cout << "Secret Key Size: " << skSize << " bytes\n";
    std::cout << "Eval Key Size: " << ekSize << " bytes\n";

    // Step 2: Generate plaintext vectors
    std::vector<std::vector<int64_t>> vectors;
    std::default_random_engine generator;
    std::uniform_int_distribution<int64_t> distribution(1, 10);

    std::cout << "Plaintext Vectors:\n";
    for (int i = 0; i < 10; ++i) {
        std::vector<int64_t> tempVector(5);
        for (int j = 0; j < 5; ++j) {
            tempVector[j] = distribution(generator);
        }
        vectors.push_back(tempVector);

        std::cout << "Vector " << i + 1 << ": ";
        for (auto val : tempVector) {
            std::cout << val << " ";
        }
        std::cout << "\n";
    }

    // Step 3: Encrypt the vectors
    std::vector<Ciphertext<DCRTPoly>> ciphertexts;
    start = Clock::now();
    for (const auto& vec : vectors) {
        Plaintext plaintext = cryptoContext->MakePackedPlaintext(vec);
        ciphertexts.push_back(cryptoContext->Encrypt(keyPair.publicKey, plaintext));
    }
    end = Clock::now();
    std::cout << "Encryption Time: "
              << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() << " ms\n";

    // Step 4: Aggregate ciphertexts
    start = Clock::now();
    auto aggregatedCiphertext = ciphertexts[0];
    for (size_t i = 1; i < ciphertexts.size(); ++i) {
        aggregatedCiphertext = cryptoContext->EvalAdd(aggregatedCiphertext, ciphertexts[i]);
    }
    end = Clock::now();
    std::cout << "Evaluation (Addition) Time: "
              << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() << " ms\n";

    // Step 5: Decrypt the aggregated result
    Plaintext plaintextAggregateResult;
    start = Clock::now();
    cryptoContext->Decrypt(keyPair.secretKey, aggregatedCiphertext, &plaintextAggregateResult);
    end = Clock::now();
    std::cout << "Decryption Time: "
              << std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count() << " ms\n";

    std::cout << "\nAggregated Result: " << plaintextAggregateResult << "\n";

    return 0;
}
