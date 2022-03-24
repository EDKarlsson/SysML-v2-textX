# SysML v2 Grammar Parser

## Development Notes
Current work is focused on the `root` layer/library of the Kernel Modeling Language.
There is a script `visualize_model.sh` that will run on a provided grammar and language file.
example:
```shell
/visualize_model.sh generate root.tx baseline.kerml verbose
```
This will generate a `dot` file in `./kerml/root/` that can be viewed if Graphviz is installed.

## Resources and Links
These are resources and links to information used while developing this project

#### Useful Tools
- [AST Explorer Webapp](https://www.astexplorer.net/)
#### Useful Github Repos
- [Dmitry Soshnikov - Syntax](https://github.com/DmitrySoshnikov/syntax)
  - "Syntactic analysis toolkit, language-agnostic parser generator."
- [GoJS - JS Diagram Lib](https://gojs.net)
#### Links
- [Wikipedia - Metamodeling](https://en.wikipedia.org/wiki/Metamodeling )
- [Geeksforgeeks - recursive descent parser](https://www.geeksforgeeks.org/recursive-descent-parser/)
#### Articles
- [Abstract vs Concrete Syntax Trees](https://eli.thegreenplace.net/2009/02/16/abstract-vs-concrete-syntax-trees/)
#### Papers
- [Model-Driven Analysis and Synthesis of Concrete Syntax](https://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.97.8081&rep=rep1&type=pdf)
- [Integrated Definition of Abstract and Concrete
  Syntax for Textual Languages](https://arxiv.org/ftp/arxiv/papers/1409/1409.6624.pdf)
#### Academic Course Materials
- [East Carolina University CSCI 5220 - Program Translation and Compiling](http://www.cs.ecu.edu/karl/5220/spr16/Notes/index.html)
#### Parsing Algorithms
- [Stereobooster - An-overview-of-parsing-algorithms](https://stereobooster.com/posts/an-overview-of-parsing-algorithms/)

# Credits

Initial project layout generated with `textx startproject`.
