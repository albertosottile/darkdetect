#import <Foundation/Foundation.h>

extern NSString * const OBSERVED_KEY;

@interface Observer : NSObject

- (void)observeValueForKeyPath:(NSString *)keyPath
                      ofObject:(id)object
                        change:(NSDictionary *)change
                       context:(void *)context;

- (void)run;

@end