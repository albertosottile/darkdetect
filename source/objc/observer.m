#import "observer.h"

NSString * const OBSERVED_KEY = @"AppleInterfaceStyle";

void signalCallback(int sig) {
    exit(sig);
}

@implementation Observer

- (id)init {
    self = [super init];
    NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
    [defaults addObserver:self forKeyPath:OBSERVED_KEY
            options:NSKeyValueObservingOptionNew
            context:nil];
    return self;
}

- (void)dealloc {
    NSUserDefaults *defaults = [NSUserDefaults standardUserDefaults];
    [defaults removeObserver:self forKeyPath:OBSERVED_KEY context:nil];
    [super dealloc];
}

- (void)observeValueForKeyPath:(NSString *)keyPath
                      ofObject:(id)object
                        change:(NSDictionary *)change
                       context:(void *)context {

    id result = change[NSKeyValueChangeNewKey];
    NSString *output;
    if (result == [NSNull null]) {
        output = @"Light";
    } else {
        output = @"Dark";
    }
    printf("Result = %s\n", [output UTF8String]);
    [[NSFileManager defaultManager] createFileAtPath:@"./objt.txt" contents:nil attributes:nil];
    [output writeToFile:@"./objt.txt" atomically:YES encoding:NSUTF8StringEncoding error:nil];

}

- (void)run {
    signal(SIGINT, signalCallback);

    NSRunLoop *runLoop = [NSRunLoop currentRunLoop];
    [runLoop run];

    printf("objc: done\n");

}

@end