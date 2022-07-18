/*
 * To compile objective-c on the command line:
 *
 * gcc -framework Foundation objc-gcc.m
 *
 * You may have to link with -lobjc or other libs,
 * as required.
 */

#import <Foundation/Foundation.h>
#import <AppKit/AppKit.h>

int main(int argc, char** argv)
{
  NSAutoreleasePool *pool = [NSAutoreleasePool alloc];
  [pool init];
  NSLog(@"Testing");
  NSString *osxMode = [[NSUserDefaults standardUserDefaults] stringForKey:@"AppleInterfaceStyle"];
  NSLog(@"Mode = %@", osxMode);
  [pool release];
}
