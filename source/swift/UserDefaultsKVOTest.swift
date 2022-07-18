import Foundation
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
        //print("\(keyPath!) value did change: \(change!)")
        let result = change?[.newKey] ?? ""
        var theme : String = String(describing: result)
        if (theme == "<null>") {
            theme = "Light"
        }
        print("Detected \(theme)")
    }
}

// Begin observing standardUserDefaults.
let observer = Observer()

RunLoop.main.run()
