package craite_test
import (
"testing"
"github.com/CRAITE-CODE/craite/sdks/go"
)
func TestNewClient(t *testing.T) {
client := craite.NewClient("test-key")
if client.APIKey != "test-key" {
t.Errorf("Expected APIKey to be 'test-key', got %s", client.APIKey)
}
}
