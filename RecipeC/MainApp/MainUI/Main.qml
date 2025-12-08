import QtQuick 2.15
import QtQuick.Controls 2.15

//Main.qml

ApplicationWindow {
    id: mainWindow
    visible: true

    width: Screen.width    // full screen width
    height: Screen.height
    visibility: Window.Maximized
    color: Theme.background

    property real font_scale: mainWindow.width / 1920
    
    Sidebar {
        id: sidebar
        onPageSelected: function(pagePath) { loader.source = pagePath }
    }

    Loader {
        id: loader
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.left: sidebar.right
        anchors.right: parent.right
        
        source: "Pages/Home.qml"
    }

}