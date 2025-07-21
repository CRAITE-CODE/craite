export class OpenZeppelinTool {
  name = 'openzeppelin';
  description = 'OpenZeppelin secure contract templates';
  
  async getContext(prompt: string): Promise<string> {
    // Return relevant OpenZeppelin patterns based on prompt
    if (prompt.includes('ERC20') || prompt.includes('token')) {
      return `Use OpenZeppelin ERC20 implementation:
import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";`;
    }
    return '';
  }
}
