int pre_increment() {
    int a = 0;
    int b = 0;
    int c = 0;
    a = ++b + c;
    return a;
}

int post_increment() {
    int a = 0;
    int b = 0;
    int c = 0;
    a = b++ + c;
    return pre_increment();
}

int main() {
    int i = pre_increment();
    int j = post_increment();
    return j;
}
