import Foundation

private var callback: ((Int)->Void)? = nil

@_silgen_name("set_callback")
public func setCallback(pointerToCTypesFunction: UnsafeMutablePointer<(Int)->Void>) {
    print("swift: setting callback")
    callback = pointerToCTypesFunction.pointee
}

let key = "AppleInterfaceStyle"

class Observer: NSObject {
    override init() {
        super.init()
        UserDefaults.standard.addObserver(self, forKeyPath: key, options: [NSKeyValueObservingOptions.new], context: Optional<UnsafeMutableRawPointer>.none)
    }

    deinit {
        UserDefaults.standard.removeObserver(self, forKeyPath: key, context: Optional<UnsafeMutableRawPointer>.none)
    }

    override func observeValue(forKeyPath keyPath: String?, of object: Any?, change: [NSKeyValueChangeKey : Any]?, context: UnsafeMutableRawPointer?) {
        //print("swift: \(keyPath!) value did change: \(change!)")
        let result = change?[.newKey] ?? ""
        let theme : String = String(describing: result)
        var ret : Int = 0
        if (theme == "<null>") {
            ret = 0
        }
        else if (theme == "Dark") {
            ret = 1
        }
        print("swift: detected \(ret)")
        if let callback = callback {
            callback(ret)
        }
    }
}

@_silgen_name("start")
public func start() -> Void {
    let signalCallback: sig_t = { signal in
        exit(signal)
    }

    signal(SIGINT, signalCallback)

    // Begin observing standardUserDefaults.
    let observer = Observer()
    _ = observer // silence "constant never used" warning

    RunLoop.current.run()
}
