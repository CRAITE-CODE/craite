# CRAITE Go SDK

Web3 AI development in Go.

## Installation

```bash
go get github.com/CRAITE-CODE/craite/sdks/go
Usage
gopackage main

import (
    "fmt"
    "log"
    
    "github.com/CRAITE-CODE/craite/sdks/go"
)

func main() {
    client := craite.NewClient("your-api-key")
    
    result, err := client.Generate("Create an ERC-20 token")
    if err != nil {
        log.Fatal(err)
    }
    
    fmt.Println(result.Code)
}
