import QtQuick 2.15

Rectangle {
    id: modalOverlay
    anchors.fill: parent

    visible: false
    color: Theme.overlay_bg

    MouseArea {
        anchors.fill: parent
        enabled: true
        propagateComposedEvents: false
    }

    Rectangle {
        anchors.centerIn: parent

        width: parent.width * 0.5
        height: parent.height * 0.5

        color: Theme.card_bg
    }
}