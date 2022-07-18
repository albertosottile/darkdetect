import Foundation

extension Notification.Name {
    static let AppleInterfaceThemeChangedNotification = Notification.Name("AppleInterfaceThemeChangedNotification")
}

class Observer: NSObject {

    func listenToInterfaceChangesNotification() {
        DistributedNotificationCenter.default.addObserver(
            self,
            selector: #selector(interfaceModeChanged),
            name: .AppleInterfaceThemeChangedNotification,
            object: nil
        )
    }

    @objc func interfaceModeChanged() {
        print("swift: detected change")
    }

}

public func main() -> Void {
    // Begin observing standardUserDefaults.
    let observer = Observer()
    observer.listenToInterfaceChangesNotification()
    //while(!observer.interrupt) {}
    RunLoop.main.run()
}

main()
