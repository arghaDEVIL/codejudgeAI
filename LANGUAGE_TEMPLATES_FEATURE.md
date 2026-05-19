# Language Templates Feature

## 🎯 Overview

When users switch programming languages in the collaborative room, they now get language-specific boilerplate code with proper structure and driver functions.

## ✨ Features

### 1. **Smart Template Loading**
- Templates load automatically when switching languages
- Only loads if editor is empty or has default content
- Preserves existing code if user has already written something
- Syncs template to all connected users

### 2. **Language-Specific Templates**

#### 🐍 Python
```python
# Python Solution
def solution():
    """
    Write your solution here
    """
    pass

if __name__ == "__main__":
    result = solution()
    print(result)
```

#### 📜 JavaScript
```javascript
// JavaScript Solution
function solution() {
    /**
     * Write your solution here
     */
    
}

// Test your solution
console.log(solution());
```

#### 📘 TypeScript
```typescript
// TypeScript Solution
function solution(): any {
    /**
     * Write your solution here
     */
    
}

// Test your solution
console.log(solution());
```

#### ☕ Java
```java
// Java Solution
public class Solution {
    public static void main(String[] args) {
        Solution sol = new Solution();
        // Test your solution
        System.out.println(sol.solution());
    }
    
    public Object solution() {
        // Write your solution here
        return null;
    }
}
```

#### ⚡ C++
```cpp
// C++ Solution
#include <iostream>
#include <vector>
#include <string>

using namespace std;

class Solution {
public:
    void solution() {
        // Write your solution here
        
    }
};

int main() {
    Solution sol;
    sol.solution();
    return 0;
}
```

#### 🔧 C
```c
// C Solution
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void solution() {
    // Write your solution here
    
}

int main() {
    solution();
    return 0;
}
```

#### 💎 C#
```csharp
// C# Solution
using System;
using System.Collections.Generic;
using System.Linq;

public class Solution {
    public static void Main(string[] args) {
        Solution sol = new Solution();
        // Test your solution
        Console.WriteLine(sol.SolutionMethod());
    }
    
    public object SolutionMethod() {
        // Write your solution here
        return null;
    }
}
```

#### 🐹 Go
```go
// Go Solution
package main

import (
    "fmt"
)

func solution() {
    // Write your solution here
    
}

func main() {
    solution()
}
```

#### 🦀 Rust
```rust
// Rust Solution
fn solution() {
    // Write your solution here
    
}

fn main() {
    solution();
}
```

## 🔄 How It Works

### 1. **Initial Load**
- Room opens with Python template by default
- Template is loaded into the editor
- All users see the same initial template

### 2. **Language Switch**
- User selects a new language from dropdown
- System checks if current code is default/empty
- If yes: Loads new language template
- If no: Keeps existing code (preserves user work)
- Syncs change to all connected users

### 3. **Template Detection**
Code is considered "default" if it:
- Is empty (`''`)
- Equals `'# Start coding here...'`
- Starts with `'# Start coding here'`
- Starts with `'// Start coding here'`
- Starts with `'/* Start coding here'`

### 4. **Synchronization**
- Template changes sync via WebSocket
- All users see the new template
- Code version increments
- Database stores the new code

## 🎨 UI Indicators

### Template Hint
- Displayed in editor toolbar
- Text: "• Templates available"
- Subtle gray color
- Informs users about the feature

## 💡 Benefits

### For Users:
✅ **No Setup Required**: Start coding immediately
✅ **Proper Structure**: Correct imports and boilerplate
✅ **Driver Functions**: Ready-to-use main/test functions
✅ **Language-Specific**: Follows language conventions
✅ **Time Saving**: No need to write boilerplate

### For Collaboration:
✅ **Consistent Structure**: All users start with same template
✅ **Clear Entry Point**: Obvious where to write code
✅ **Professional**: Looks polished and organized
✅ **Educational**: Shows proper code structure

## 🔧 Technical Implementation

### Function: `getLanguageTemplate(lang)`
- Takes language code as parameter
- Returns appropriate template string
- Includes proper comments and structure
- Has driver/main function for testing

### Function: `handleLanguageChange(newLang)`
- Checks if current code is default
- Loads template if appropriate
- Syncs to all users via WebSocket
- Updates editor language mode

### State Management:
- `language`: Current selected language
- `code`: Current editor content
- Templates loaded on-demand
- Synced via `sendCodeChange()`

## 🎯 Use Cases

### 1. **New Room**
- User creates room
- Python template loads automatically
- Ready to start coding

### 2. **Language Switch (Empty Editor)**
- User switches to JavaScript
- JavaScript template loads
- Boilerplate ready

### 3. **Language Switch (With Code)**
- User has written Python code
- Switches to JavaScript
- Code preserved (no template load)
- User manually adapts code

### 4. **Multi-User Scenario**
- User A switches language
- Template syncs to User B
- Both see new template
- Can start collaborating immediately

## 📊 Template Structure

All templates include:
1. **Comment Header**: Language name
2. **Function/Class**: Main solution container
3. **Documentation**: Comment placeholders
4. **Driver Code**: Main/test function
5. **Proper Imports**: Common libraries (where applicable)

## 🚀 Future Enhancements

Potential improvements:
- [ ] Problem-specific templates
- [ ] Custom template library
- [ ] Template preferences per user
- [ ] More language support
- [ ] Code snippets library
- [ ] Template versioning

## ✅ Testing

### Test Scenarios:
1. ✅ Create new room → Python template loads
2. ✅ Switch language (empty) → New template loads
3. ✅ Switch language (with code) → Code preserved
4. ✅ Multi-user sync → All users see template
5. ✅ Reconnect → Template persists
6. ✅ All 9 languages → Templates load correctly

## 🎊 Result

Users now have a professional coding experience with proper boilerplate code for every supported language, making it easier to start coding and collaborate effectively!
