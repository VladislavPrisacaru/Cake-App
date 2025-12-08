import QtQuick 2.15
import QtQuick.Controls 2.15

//SidebarButton.qml

Button {
    id: nav_button

    property string label: ""
    property string pageName: ""
    property bool isActive: sidebar.currentPage === pageName

    onClicked: { 
        sidebar.currentPage = pageName 
        sidebar.pageSelected(pageName)
    }
    
    background: Rectangle {
        id: bg
        anchors.fill: parent
        color: "transparent"

        Rectangle {
            id: fill_anim
            color: Theme.sidebar_active
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            width: 0

            states: [
                State {
                    name: "expand"
                    when: nav_button.isActive
                    PropertyChanges { target: fill_anim; width: bg.width}
                },
                State {
                    name: "collapse"
                    when: !nav_button.isActive
                    PropertyChanges { target: fill_anim; width: 0}
                }
            ]

            transitions: [
                Transition {
                    NumberAnimation {
                        properties: "width"
                        duration: 170
                        easing.type: Easing.InCirc
                    }
                }
            ]
        }

        Rectangle {
            id: glowbar
            width: parent.width * 0.02
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom

            color: nav_button.hovered || nav_button.isActive ? Theme.sidebar_hover : "transparent"
            Behavior on color {
                ColorAnimation { duration: 150}
            }
        }
    }

    contentItem: Item {
        Text {
            anchors.left: parent.left
            anchors.leftMargin: parent.width * 0.15
            anchors.verticalCenter: parent.verticalCenter
            text: nav_button.label

            color: nav_button.isActive ? Theme.sidebar_text_active : Theme.sidebar_text
            font.family: Theme.font_family
            font.pointSize: Theme.font_size_normal * font_scale
            
        }
    }
}