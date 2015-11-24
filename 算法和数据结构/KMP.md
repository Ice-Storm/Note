KMP 算法简介
===========

KMP 算法是一种字符串匹配算法。
```cpp
#include <iostream>
#include <map>
#include <vector>

using namespace std;

/**  
 *		原始版本
 */
int kmp(const string& src, const string& dest) { 
    if(dest.length()>src.length()) return -1;
    vector<int> next;  // store length of common string
    next.push_back(0);
    next.push_back(0);
    for (int i = 1; i < dest.length(); ++i) {
        int j = i;
        while (j > 0) {
            if (dest[next[j]] == dest[i]) {
                next.push_back(next[j] + 1);
                break;
            } else {
                j = next[j];
            }
        }
        if(j==0) next.push_back(0);
    }
    int j = 0;
    for (int i = 0; i < src.length(); ++i) {
        while(1) {
            if (dest[j] == src[i]) {
                ++j;
                break;
            } else {
                if(j==0) break;
                j = next[j];
            }
        }
        if(j==dest.length()) return i-j+1;
    }
    return -1;

}
/**
 *		精简代码
 */
int kmp2(const string &src, const string &dest) {
    if (dest.length() > src.length()) {
        return -1;
    }
    int *next = new int[dest.length()+1];
    next[0] = next[1] = 0;
    for (int i = 1; i < dest.length(); ++i) {
        int j = next[i];
        while(j>0&&dest[j]!=dest[i]) j = next[j];
        if(dest[j]==dest[i]) {
            next[i+1] = j+1;
        } else {
            next[i+1] = 0;
        }
    }
    int j = 0;
    for (int i = 0; i < src.length(); ++i) {
        while(j>0&&dest[j]!=src[i]) j = next[j];
        if(dest[j]==src[i]){
            ++j;
        } else {
            // pass
        }
        if(j==dest.length()) return i-j+1;

    }
    return -1;
}

/**
 *  优化 next 数组。
 */
int kmp3(const string &src, const string &dest) {
    if (dest.length() > src.length()) {
        return -1;
    }
    int *next = new int[dest.length() + 1];
    next[0] = next[1] = 0;
    for (int i = 1; i < dest.length()-1; ++i) {
        int j = next[i];
        while (j > 0 && dest[j] != dest[i]) j = next[j];
        if (dest[j] == dest[i]) {
            if (dest[j + 1] != dest[i + 1]) { 
            // 优化 next 数组,如果当前dest[i]和dest[j]的下一位置也相同,则说明当                                  
            // dest 在 位置i+1 失配的时候,再去匹配位置j+1也会失配,因此next[i+1]赋值成j+1
            // 有点多余,直接把 next[i+1]赋值成 next[j+1].}

                next[i + 1] = j + 1;
            } else {
                next[i + 1] = next[j+1];
            }
        } else {
            next[i + 1] = 0;
        }
    }
    int j = 0;
    for (int i = 0; i < src.length(); ++i) {
        while (j > 0 && dest[j] != src[i]) j = next[j];
        if (dest[j] == src[i]) {
            ++j;
        } else {
            // pass
        }
        if (j == dest.length()) return i - j + 1;
    }
    return -1;
}
/**
 *		优化 Next 数组
 */
void getNextUpdate(const std::string& p, std::vector<int>& next)
{
    next.resize(p.size());
    next[0] = -1;

    int i = 0, j = -1;

    while (i != p.size() - 1)
    {
        //这里注意，i==0的时候实际上求的是nextVector[1]的值，以此类推
        if (j == -1 || p[i] == p[j])
        {
            ++i;
            ++j;
            //update
            //next[i] = j;
            //注意这里是++i和++j之后的p[i]、p[j]
            next[i] = p[i] != p[j] ? j : next[j];
        }
        else
        {
            j = next[j];
        }
    }
}

int main() {
    const char *src = "abcabcb";
    int i = kmp3(src, "bcb");
    cout<<src+i<<endl;
    vector<int> next;

    return 0;
}
```

