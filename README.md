1. What design pattern best improves this code?
    Command

2. What role does each major class play in that pattern?
    Each class is encapsulating a command as an object rather than a method 

3. Why is this refactoring better than the original design?
    In the original design, there was a large block of if-else statements, and every new command had to be integrated into that if-else block. Several different methods are squished into one class, violating the principle of SOLID's single responsibility principle. The command design allows for us to add new functions much more easily 