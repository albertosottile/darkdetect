/*
 * To compile objective-c on the command line:
 *
 * clang -framework Foundation objc_listener.m observer.m -o hello
 *
 * You may have to link with -lobjc or other libs,
 * as required.
 */

#import <Foundation/Foundation.h>
#import <AppKit/AppKit.h>
#import <signal.h>
#import "observer.h"

void signalCallback(int sig) {
    exit(sig);
}

void start()
{

  @autoreleasepool {
    signal(SIGINT, signalCallback);

    NSLog(@"Testing");

    Observer *observer = [[Observer alloc] init];

    NSRunLoop *runLoop = [NSRunLoop currentRunLoop];
    [runLoop run];
  }
}
