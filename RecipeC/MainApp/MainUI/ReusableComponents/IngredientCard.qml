// IngredientCard.qml
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import QtQuick.Effects

Item {
    id: wrapper

    property string ingredient_name: "Name"
    property string category: "Category"
    property int n_recipes: 123
    property int total_price: 123
    property string price_unit: "£"
    property int total_weight: 123
    property string weight_unit: "g"

    implicitWidth: ingredient_page.width * 0.25
    implicitHeight: ingredient_page.width * 0.15

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

        ColumnLayout {
            anchors.fill: parent
            anchors.leftMargin: wrapper.width * 0.07
            anchors.rightMargin: wrapper.width * 0.07
            anchors.bottomMargin: wrapper.width * 0.07
            anchors.topMargin: wrapper.width * 0.04
            spacing: wrapper.height * 0.035

            Text {
                text: wrapper.ingredient_name
                color: Theme.text_primary
                font.pointSize: Theme.font_size_heading_small * font_scale
                font.bold: true
                Layout.fillWidth: true
            }

            Rectangle {
                
                Layout.preferredHeight: category_txt.implicitHeight * 1.25
                Layout.preferredWidth: category_txt.implicitWidth * 1

                Text {
                    id: category_txt
                    anchors.centerIn: parent
                    //leftPadding: wrapper.width * 0.005
                    text: wrapper.category
                    color: Theme.text_secondary
                    font.pointSize: Theme.font_size_small * font_scale
                }
            }
            
            Rectangle {
                
                Layout.preferredHeight: n_recipes_txt.implicitHeight * 1.25
                Layout.preferredWidth: n_recipes_txt.implicitWidth * 1.2

                color: Theme.n_recipes_bg
                radius: Theme.radius_small

                Text {
                    id: n_recipes_txt
                    anchors.centerIn: parent
                    leftPadding: wrapper.width * 0.02
                    text: `Used in ${wrapper.n_recipes} recipes`
                    color: Theme.text_secondary
                    font.pointSize: Theme.font_size_small * font_scale
                }
            }

            RowLayout {

                Layout.fillWidth: true
                spacing: wrapper.width * 0.22

                ColumnLayout {
                    Layout.fillWidth: true

                    Text {
                        text: "TOTAL PRICE"
                        color: Theme.text_secondary
                        font.pointSize: Theme.font_size_small * font_scale
                    }

                    Text {
                        text: `${price_unit}${total_price}`
                        color: Theme.price_green
                        font.pointSize: Theme.font_size_heading_small * font_scale
                        font.bold: true
                    }
                }

                ColumnLayout {
                    Layout.fillWidth: true

                    Text {
                        text: "TOTAL WEIGHT"
                        color: Theme.text_secondary
                        font.pointSize: Theme.font_size_small * font_scale
                    }

                    Text {
                        text: `${total_weight} ${weight_unit}`
                        color: Theme.weight_blue
                        font.pointSize: Theme.font_size_heading_small * font_scale
                        font.bold: true
                    }
                }
            }

            RowLayout {

                Layout.fillWidth: true
                spacing: wrapper.width * 0.02               

                Button {

                    Layout.fillWidth: true
                    Layout.preferredHeight: wrapper.height * 0.22

                    background: Rectangle {
                        anchors.fill: parent
                        color: Theme.btn_primary
                        radius: Theme.radius_small
                        
                        MouseArea {
                            anchors.fill: parent
                            hoverEnabled: true

                            onEntered: parent.color = Theme.btn_primary_hover
                            onExited: parent.color = Theme.btn_primary
                        }

                        Behavior on color {
                            ColorAnimation { duration: 200; easing.type: Easing.InOutQuad }
                        }
                    }

                    contentItem: Item {
                        Text {
                            anchors.centerIn: parent
                            text: "Edit"

                            color: Theme.sidebar_text_active
                            font.family: Theme.font_family
                            font.pointSize: Theme.font_size_normal * font_scale
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                        }
                    }
                }

                Button {
                    id: delete_btn

                    Layout.fillWidth: true
                    Layout.preferredHeight: wrapper.height * 0.22

                    background: Rectangle {
                        anchors.fill: parent
                        color: Theme.card_bg
                        border.width: 2
                        border.color: delete_btn.hovered ? Theme.card_border_hover : Theme.card_border
                        radius: Theme.radius_small
                    }

                    contentItem: Item {
                        Text {
                            anchors.centerIn: parent
                            text: "Delete"

                            color: Theme.text_primary
                            font.family: Theme.font_family
                            font.pointSize: Theme.font_size_normal * font_scale
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter  
                        }
                    }
                }
            }
        }
    }
}
