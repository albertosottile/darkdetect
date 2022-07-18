Build libraries with e.g.
`clang -framework Foundation -shared -undefined dynamic_lookup -o libObserver.dylib observer.m`

Build stand-alone executables with e.g.
`clang -framework Foundation objc_listener.m observer.m -o hello`
