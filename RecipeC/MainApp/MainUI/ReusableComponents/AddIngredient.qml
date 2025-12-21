import QtQuick 2.15
import QtQuick.Layouts 2.15
import QtQuick.Controls 2.15
import QtQuick.Effects


Rectangle {
    id: modal_overlay

    property string mode_txt: "Add Ingredient"

    anchors.fill: parent

    visible: false
    color: Theme.overlay_bg

    MouseArea {
        anchors.fill: parent
        enabled: true
        propagateComposedEvents: false
    }

    RectangularShadow {
        anchors.fill:  overlay_rectangle
        radius:  overlay_rectangle.radius
        blur:  overlay_rectangle.height * 0.06
        spread: 0.6
        color: Qt.darker("#88000000", 1.0)
    }

    Rectangle {
        id: overlay_rectangle
        anchors.centerIn: parent

        width: parent.width * 0.3
        height: parent.height * 0.6

        color: Theme.card_bg
        radius: Theme.radius_small

        ColumnLayout {
            id: add_ingredient_column

            anchors.fill: parent
            spacing: ingredient_page.height * 0.02
            anchors.margins: ingredient_page.width * 0.018

            Text { // header
                text: modal_overlay.mode_txt
                font.bold: true
                color: Theme.text_primary
                font.family: Theme.font_family
                font.pointSize: Theme.font_size_normal * font_scale
                Layout.fillWidth: true
                horizontalAlignment: Text.AlignHCenter
            }

            Item {Layout.preferredHeight: ingredient_page.height * 0.005}

            ColumnLayout {
                id: labeled_field

                Layout.fillWidth: true
                spacing: ingredient_page.height * 0.015

                Text {
                    text: "Ingredient Name"
                    color: Theme.text_primary
                    font.family: Theme.font_family
                    font.pointSize: Theme.font_size_normal * font_scale
                    Layout.fillWidth: true
                }

                TextField {
                    id: text_field

                    Layout.fillWidth: true

                    Layout.preferredHeight: modal_overlay.height * 0.042
                    
                    background: Rectangle {
                        border.color: text_field.activeFocus ? Theme.card_border_hover : text_field.hovered ? Theme.card_border_hover : Theme.card_border_dark
                        color: Theme.card_bg   
                        radius: Theme.radius_tiny
                        border.width: 2
                    }

                    placeholderText: "Flour, Sugar etc."
                    placeholderTextColor: Theme.text_placeholder
                    color: Theme.text_primary
                    font.family: Theme.font_family
                    font.pointSize: Theme.font_size_normal * font_scale 
                }

                Loader  {
                    sourceComponent: labeled_field_combo
                    Layout.fillWidth: true
                    
                    onLoaded: {
                        item.label = "Ingredient Weight"
                        item.placeholder = "..."
                        item.combo_values = ["g", "kg", "ml", "l", "oz", "lb"]
                    }
                }

                Loader  {
                    sourceComponent: labeled_field_combo
                    Layout.fillWidth: true
                    
                    onLoaded: {
                        item.label = "Ingredient Weight"
                        item.placeholder = "..."
                        item.combo_values = ["£", "€", "$"]
                    }
                }

                ColumnLayout {
                    id: category_combo_column

                    Layout.fillWidth: true
                    spacing: ingredient_page.height * 0.015

                    Text {
                        text: "Ingredient Categories"
                        color: Theme.text_primary
                        font.family: Theme.font_family
                        font.pointSize: Theme.font_size_normal * font_scale
                        Layout.fillWidth: true
                    }

                    ComboBox {
                        id: categorie_combo
                        model: ["All Categories", "Dairy",  "Baking Ingredients", "Fruits", "Grains", "Meat & Seafood", "Vegetables", "Other"]

                        Layout.fillWidth: true
                        Layout.preferredHeight: ingredient_page.height * 0.045

                        popup: Popup {
                            y: categorie_combo.height 
                            width: categorie_combo.width
                            height: Math.min(ingredient_page.height * 0.03 * categorie_combo.model.length, 
                                            ingredient_page.height * 0.4)
                            padding: ingredient_page.height * 0.003
                            
                            background: Rectangle {
                                color: Theme.background
                                radius: Theme.radius_small
                                border.width: 2
                                border.color: Theme.card_border
                            }

                            contentItem: ListView {
                                clip: true
                                implicitHeight: contentHeight
                                model: categorie_combo.popup.visible ? categorie_combo.delegateModel : null
                                currentIndex: categorie_combo.highlightedIndex
                            }
                        }

                        indicator: Image {
                            source: "../../Utils/Images/black_arrow.svg"
                            width: Math.round(ingredient_page.width * 0.02 * Screen.devicePixelRatio)
                            height: Math.round(ingredient_page.height * 0.03 * Screen.devicePixelRatio)
                            anchors.right: parent.right
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.rightMargin: ingredient_page.width * 0.015

                        }

                        background: Rectangle {
                            anchors.fill: parent
                            color: Theme.card_bg
                            radius: Theme.radius_small
                            border.width: 2
                            border.color: categorie_combo.hovered ? Theme.card_border_hover : categorie_combo.hovered ? Theme.card_border_hover : Theme.card_border_dark
                        }

                        contentItem: Item {
                            Text {
                                anchors.centerIn: parent
                                text: categorie_combo.displayText
                                color: Theme.text_primary
                                font.family: Theme.font_family
                                font.pointSize: Theme.font_size_normal * font_scale
                                verticalAlignment: Text.AlignVCenter
                                elide: Text.ElideMiddle
                            }
                        }

                        delegate: ItemDelegate {
                            width: categorie_combo.width
                            height: ingredient_page.height * 0.03

                            contentItem: Item {
                                anchors.fill: parent
                                Text {
                                    anchors.fill: parent
                                    text: modelData
                                    color: hovered ? Theme.card_bg : Theme.text_primary
                                    font.family: Theme.font_family
                                    font.pointSize: Theme.font_size_normal * font_scale
                                    verticalAlignment: Text.AlignVCenter
                                    horizontalAlignment: Text.AlignHCenter
                                    elide: Text.ElideMiddle
                                }
                            }

                            background: Rectangle {
                                color: hovered ? Theme.btn_primary : Theme.card_bg
                                radius: 3
                                Behavior on color {
                                    ColorAnimation { duration: 200; easing.type: Easing.InOutQuad }
                                }
                            }
                        }
                    }
                }

                Item {Layout.preferredHeight: modal_overlay.height * 0.02}

                RowLayout {

                    Layout.fillWidth: true
                    spacing: modal_overlay.height * 0.015

                    Button {
                        id: modal_save_btn

                        Layout.fillWidth: true
                        Layout.preferredHeight: modal_overlay.height * 0.05

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
                                text: "Save"

                                color: Theme.sidebar_text_active
                                font.family: Theme.font_family
                                font.pointSize: Theme.font_size_normal * font_scale
                                verticalAlignment: Text.AlignVCenter
                                horizontalAlignment: Text.AlignHCenter
                            }
                        }
                    }

                    Button {
                        id: modal_delete_btn

                        Layout.fillWidth: true
                        Layout.preferredHeight: modal_overlay.height * 0.05

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
                                text: "Delete"

                                color: Theme.sidebar_text_active
                                font.family: Theme.font_family
                                font.pointSize: Theme.font_size_normal * font_scale
                                verticalAlignment: Text.AlignVCenter
                                horizontalAlignment: Text.AlignHCenter
                            }
                        }
                    }

                    Button {
                        id: modal_cancel_btn

                        Layout.fillWidth: true
                        Layout.preferredHeight: modal_overlay.height * 0.05

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
                                text: "Cancel"

                                color: Theme.sidebar_text_active
                                font.family: Theme.font_family
                                font.pointSize: Theme.font_size_normal * font_scale
                                verticalAlignment: Text.AlignVCenter
                                horizontalAlignment: Text.AlignHCenter
                            }
                        }
                    }
                }

                Item {Layout.fillHeight: true}
            }
            
            Component {
                id: labeled_field_combo

                ColumnLayout {
                    id: labeled_field_column

                    property string label
                    property string placeholder
                    property bool combo: true
                    property var combo_values: []

                    Layout.fillWidth: true
                    spacing: ingredient_page.height * 0.015

                    Text {
                        text: labeled_field_column.label
                        color: Theme.text_primary
                        font.family: Theme.font_family
                        font.pointSize: Theme.font_size_normal * font_scale
                        Layout.fillWidth: true
                    }

                    RowLayout {
                        id: labeled_field_row

                        Layout.fillWidth: true

                        spacing: parent.width * 0.07

                        TextField {
                            id: text_field  

                            Layout.fillWidth: true

                            Layout.preferredHeight: modal_overlay.height * 0.042
                            
                            background: Rectangle {
                                border.color: text_field.activeFocus ? Theme.card_border_hover : text_field.hovered ? Theme.card_border_hover : Theme.card_border_dark
                                color: Theme.card_bg   
                                radius: Theme.radius_tiny
                                border.width: 2
                            }

                            placeholderText: labeled_field_column.placeholder
                            placeholderTextColor: Theme.text_placeholder
                            color: Theme.text_primary
                            font.family: Theme.font_family
                            font.pointSize: Theme.font_size_normal * font_scale 
                        }

                        ComboBox {
                            id: categorie_combo
                            model: labeled_field_column.combo_values

                            Layout.preferredWidth: parent.width * 0.25
                            Layout.preferredHeight: modal_overlay.height * 0.042

                            popup: Popup {
                                y: categorie_combo.height 
                                width: categorie_combo.width
                                height: Math.min(ingredient_page.height * 0.03 * categorie_combo.model.length, 
                                                ingredient_page.height * 0.4)
                                padding: ingredient_page.height * 0.003
                                
                                background: Rectangle {
                                    color: Theme.background
                                    radius: Theme.radius_small
                                    border.width: 2
                                    border.color: Theme.card_border_dark
                                }

                                contentItem: ListView {
                                    clip: true
                                    implicitHeight: contentHeight
                                    model: categorie_combo.popup.visible ? categorie_combo.delegateModel : null
                                    currentIndex: categorie_combo.highlightedIndex
                                }
                            }

                            indicator: Image {
                                source: "../../Utils/Images/black_arrow.svg"
                                width: Math.round(ingredient_page.width * 0.02 * Screen.devicePixelRatio)
                                height: Math.round(ingredient_page.height * 0.03 * Screen.devicePixelRatio)
                                anchors.right: parent.right
                                anchors.verticalCenter: parent.verticalCenter
                                anchors.rightMargin: ingredient_page.width * 0.005

                            }

                            background: Rectangle {
                                anchors.fill: parent
                                color: Theme.card_bg
                                radius: Theme.radius_small
                                border.width: 2
                                border.color: categorie_combo.hovered ? Theme.card_border_hover : categorie_combo.hovered ? Theme.card_border_hover : Theme.card_border_dark
                            }

                            contentItem: Item {
                                Text {
                                    anchors.centerIn: parent
                                    text: categorie_combo.displayText
                                    color: Theme.text_primary
                                    font.family: Theme.font_family
                                    font.pointSize: Theme.font_size_normal * font_scale
                                    verticalAlignment: Text.AlignVCenter
                                    elide: Text.ElideMiddle
                                }
                            }

                            delegate: ItemDelegate {
                                width: categorie_combo.width
                                height: ingredient_page.height * 0.03

                                contentItem: Item {
                                    anchors.fill: parent
                                    Text {
                                        anchors.fill: parent
                                        text: modelData
                                        color: hovered ? Theme.card_bg : Theme.text_primary
                                        font.family: Theme.font_family
                                        font.pointSize: Theme.font_size_normal * font_scale
                                        verticalAlignment: Text.AlignVCenter
                                        horizontalAlignment: Text.AlignHCenter
                                        elide: Text.ElideMiddle
                                    }
                                }

                                background: Rectangle {
                                    color: hovered ? Theme.btn_primary : Theme.card_bg
                                    radius: 3
                                    Behavior on color {
                                        ColorAnimation { duration: 200; easing.type: Easing.InOutQuad }
                                    }
                                }
                            }
                        }
                    }
                }
            } 
        }
    }
}