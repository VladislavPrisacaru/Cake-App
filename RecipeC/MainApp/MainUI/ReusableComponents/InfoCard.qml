// InfoCard.qml
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import QtQuick.Effects

Item {
    id: wrapper

    property string mainText: ""
    property int mainValue: 123
    property color valueColor: "white"

    implicitWidth: ingredient_page.width * 0.23
    implicitHeight: ingredient_page.width * 0.1

    RectangularShadow {
        anchors.fill: infoCard
        radius: infoCard.radius
        blur: infoCard.height * 0.10
        spread: 0.9
        color: Qt.darker(infoCard.color, 1.15)
    }

    Rectangle {
        id: infoCard
        anchors.fill: parent
        radius: Theme.radius_big
        color: Theme.card_bg
        border.width: 2
        border.color: Theme.card_border

        Column {
            anchors {
                fill: parent
                leftMargin: width * 0.08
                topMargin: height * 0.10
            }
            spacing: height * 0.05

            Text {
                text: wrapper.mainText
                color: Theme.text_secondary
                font.pointSize: Theme.font_size_small * font_scale
            }

            Text {
                text: wrapper.mainValue
                color: wrapper.valueColor
                font.bold: true
                font.pointSize: Theme.font_size_heading * font_scale
            }
        }
        Item { Layout.fillHeight: true }
    }
}
