package main
import (
"fmt"
"log"
"os"
"github.com/CRAITE-CODE/craite/sdks/go"
"github.com/joho/godotenv"
)
func main() {
// Load environment variables
godotenv.Load()
apiKey := os.Getenv("CRAITE_API_KEY")
if apiKey == "" {
    log.Fatal("CRAITE_API_KEY not set")
}

// Create client
client := craite.NewClient(apiKey)

// Generate a decentralized exchange
result, err := client.Generate("Create a Uniswap-style DEX with liquidity pools")
if err != nil {
    log.Fatal(err)
}

fmt.Printf("Generated DEX Contract:\n%s\n", result.Code)

// Save to file
err = os.WriteFile("dex.sol", []byte(result.Code), 0644)
if err != nil {
    log.Fatal(err)
}

fmt.Println("Contract saved to dex.sol")
}
