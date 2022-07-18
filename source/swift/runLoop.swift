import Foundation

@_silgen_name("run")
public func run() -> Void {
    // Some convenience code to allow interrupting with Ctrl-C from Python
    let signalCallback: sig_t = { signal in
        exit(signal)
    }

    signal(SIGINT, signalCallback)

    RunLoop.current.run()
}
