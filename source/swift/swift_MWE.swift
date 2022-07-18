import Foundation

let key = "AppleInterfaceStyle"

class Observer: NSObject {

    var started:Bool = false
    var interrupt:Bool = false

    deinit {
        if (started) {
            UserDefaults.standard.removeObserver(self, forKeyPath: key, context: Optional<UnsafeMutableRawPointer>.none)
        }
    }

    func start() {
        started = true
        UserDefaults.standard.addObserver(self, forKeyPath: key, options: [NSKeyValueObservingOptions.new], context: Optional<UnsafeMutableRawPointer>.none)
    }

    override func observeValue(forKeyPath keyPath: String?, of object: Any?, change: [NSKeyValueChangeKey : Any]?, context: UnsafeMutableRawPointer?) {
        interrupt = true
        let result = change?[.newKey] ?? ""
        var theme : String = String(describing: result)
        if (theme == "<null>") {
            theme = "Light"
        }
        print("swift: detected \(theme)")
        interrupt = false
    }
}

public func main() -> Void {
    // Begin observing standardUserDefaults.
    let observer = Observer()
    observer.start()
    //while(!observer.interrupt) {}
    RunLoop.main.run()
}

// main() //run from main thread with stdin

// run from background
DispatchQueue.global(qos: .background).async {
    main()
}

