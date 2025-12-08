import QtQuick 2.15
import QtQuick.Layouts 2.15
import QtQuick.Controls 2.15
import "../ReusableComponents"

// IngredientPage.qml

Item {
    id: ingredient_page
    anchors.fill: parent

    property int currentPage: 0
    property int itemsPerPage: 8
    property int totalPages: Math.ceil(ingredientModel.count / itemsPerPage)

    function updatePage() {
        pageModel.clear()
        let start = currentPage * itemsPerPage
        let end = Math.min(start + itemsPerPage, ingredientModel.count)

        for (let i = start; i < end; i++) {
            pageModel.append(ingredientModel.get(i))
        }
    }

    ColumnLayout {
        id: nav_column
        anchors.fill: parent
        spacing: ingredient_page.height * 0.015
        anchors.margins: ingredient_page.width * 0.018

        Layout.topMargin: ingredient_page.height * 0.025

        //header
        ColumnLayout {
            Layout.fillWidth: true
            spacing: ingredient_page.height * 0.01

            Text {
                text: "Ingredient Library"
                font.bold: true
                color: Theme.text_primary
                font.family: Theme.font_family
                font.pointSize: Theme.font_size_heading * font_scale
                Layout.fillWidth: true
            }
        
            Text {
                text: "Manage Ingredient library and pricing"
                color: Theme.text_tertiary
                font.family: Theme.font_family
                font.pointSize: Theme.font_size_small * font_scale
                Layout.fillWidth: true     
            }

            Layout.bottomMargin: ingredient_page.height * 0.022
        }

        //info card row
        RowLayout {
            Layout.fillWidth: true
            spacing: ingredient_page.width * 0.015

            InfoCard {
                Layout.fillWidth: true
                Layout.preferredHeight: ingredient_page.width * 0.08
                mainText : "TOTAL INGREDIENTS"
                valueColor: Theme.btn_primary
            }

            InfoCard {
                Layout.fillWidth: true
                Layout.preferredHeight: ingredient_page.width * 0.08
                valueColor: Theme.price_green
                mainText : "USED INGREDIENTS"
            }

            InfoCard {
                Layout.fillWidth: true
                Layout.preferredHeight: ingredient_page.width * 0.08
                valueColor: Theme.calories_yellow
                mainText : "UNUSED INGREDIENTS"
            }

            InfoCard {
                Layout.fillWidth: true
                Layout.preferredHeight: ingredient_page.width * 0.08
                valueColor: Theme.weight_blue
                mainText : "MOST USED INGREDIENT"
            }

            Layout.bottomMargin: ingredient_page.height * 0.02
        }

        RowLayout {
            
            Layout.fillWidth: true
            spacing: ingredient_page.width * 0.015

            //add ingredient button
            Button {
                id: add_ingredient_btn
                //property alias model: ingredient_page.ingredient_model

                implicitWidth: ingredient_page.width * 0.23
                implicitHeight: ingredient_page.height * 0.06

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
                        text: "+ Add Ingredient"

                        color: Theme.sidebar_text_active
                        font.family: Theme.font_family
                        font.pointSize: Theme.font_size_normal * font_scale
                        verticalAlignment: Text.AlignVCenter
                        horizontalAlignment: Text.AlignHCenter
                    }
                }

                onClicked: ingredientModel.append({name: "Name", category: "category", n_recipes: 0, total_price: 123, price_unit: "£", total_weight: 123, weight_unit: "g"})
            }

            //category combo
            ComboBox {
                id: categorie_combo
                model: ["All Categories", "Dairy",  "Baking Ingredients", "Fruits", "Grains", "Meat & Seafood", "Vegetables", "Other"]

                implicitWidth: ingredient_page.width * 0.18
                implicitHeight: ingredient_page.height * 0.06

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
                    border.color: Theme.card_border
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

            //sort combo
            ComboBox {
                id: sort_combo
                model: ["All", "Name A-Z", "Name Z-A", "Oldest", "Newest",   "Price ⯅", "Price ⯆"]

                implicitWidth: ingredient_page.width * 0.18
                implicitHeight: ingredient_page.height * 0.06

                popup: Popup {
                    y: sort_combo.height 
                    width: sort_combo.width
                    height: Math.min(ingredient_page.height * 0.03 * sort_combo.model.length, 
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
                        model: sort_combo.popup.visible ? sort_combo.delegateModel : null
                        currentIndex: sort_combo.highlightedIndex
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
                    border.color: Theme.card_border
                }

                contentItem: Row {
                    anchors.fill: parent
                    leftPadding: ingredient_page.width * 0.015
                    spacing: ingredient_page.width * 0.007

                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        text: "Sort by:"
                        color: Theme.text_primary
                        font.family: Theme.font_family
                        font.pointSize: Theme.font_size_normal * font_scale
                        verticalAlignment: Text.AlignVCenter
                    }
                    Text {
                        anchors.verticalCenter: parent.verticalCenter
                        text: sort_combo.displayText
                        color: Theme.text_primary
                        font.family: Theme.font_family
                        font.pointSize: Theme.font_size_normal * font_scale
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideMiddle
                    }
                }

                delegate: ItemDelegate {
                    width: sort_combo.width
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

            // search bar
            Rectangle {
                id: search_bar_container

                Layout.fillWidth: true
                Layout.preferredHeight: ingredient_page.height * 0.06
                color: Theme.card_bg
                radius: Theme.radius_small
                border.width: 2
                border.color: search_bar.focus ? Theme.card_border_hover : hover_handler.hovered ? Theme.card_border_hover : Theme.card_border

                HoverHandler {
                    id: hover_handler
                    target: search_bar_container
                }

                Row {

                    anchors.fill: parent
                    spacing: ingredient_page.width * 0.01
                    leftPadding: ingredient_page.width * 0.01 

                    Image {
                        source: "../../Utils/Images/search_icon.svg"
                        width: parent.height * 0.4
                        height: width
                        anchors.verticalCenter: parent.verticalCenter
                        fillMode: Image.PreserveAspectFit
                    }
                
                    TextField {
                        id: search_bar

                        placeholderText: "Search..."
                        background: null

                        anchors.verticalCenter: parent.verticalCenter
                        Layout.fillWidth: true
                          
                        placeholderTextColor: Theme.text_placeholder
                        color: Theme.text_primary
                        font.family: Theme.font_family
                        font.pointSize: Theme.font_size_normal * font_scale   
                    }
                }
            }

            Layout.bottomMargin: ingredient_page.height * 0.02
        }

        // label with page change buttons
        RowLayout {
            Layout.fillWidth: true

            spacing: ingredient_page.width * 0.02
            Layout.rightMargin: ingredient_page.width * 0.02

            Text {
                text: "INGREDIENTS"
                color: Theme.text_secondary
                font.family: Theme.font_family
                font.pointSize: Theme.font_size_small * font_scale
            }

            Item { Layout.fillWidth: true }

            Text {
                text: `Page ${currentPage + 1} / ${totalPages}`
                color: Theme.text_secondary
                font.family: Theme.font_family
                font.pointSize: Theme.font_size_small * font_scale
            }

            RowLayout {

                spacing: ingredient_page.width * 0.02

                Button {
                    id: change_page_left

                    implicitHeight: ingredient_page.height * 0.02
                    implicitWidth: ingredient_page.width * 0.019
                    

                    background: Rectangle {
                        anchors.fill: parent
                        color: change_page_left.hovered ? Theme.btn_primary_hover : Theme.btn_primary
                        radius: 3

                        Behavior on color {
                            ColorAnimation { duration: 200; easing.type: Easing.InOutQuad }
                        }
                    }

                    contentItem: Item {
                        Text {
                            anchors.centerIn: parent
                            text: "<"

                            color: Theme.sidebar_text_active
                            font.family: Theme.font_family
                            font.pointSize: Theme.font_size_normal * font_scale
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                        }
                    }

                    onClicked: {
                        if (ingredient_page.currentPage > 0) {
                            ingredient_page.currentPage--
                            ingredient_page.updatePage()
                        }
                    }
                }

                Button {
                    id: change_page_right

                    implicitHeight: ingredient_page.height * 0.02
                    implicitWidth: ingredient_page.width * 0.019
                    

                    background: Rectangle {
                        anchors.fill: parent
                        color: change_page_right.hovered ? Theme.btn_primary_hover : Theme.btn_primary
                        radius: 2

                        Behavior on color {
                            ColorAnimation { duration: 200; easing.type: Easing.InOutQuad }
                        }
                    }

                    contentItem: Item {
                        Text {
                            anchors.centerIn: parent
                            text: ">"

                            color: Theme.sidebar_text_active
                            font.family: Theme.font_family
                            font.pointSize: Theme.font_size_normal * font_scale
                            verticalAlignment: Text.AlignVCenter
                            horizontalAlignment: Text.AlignHCenter
                        }
                    }
                    onClicked: {
                        if (ingredient_page.currentPage < totalPages - 1) {
                                ingredient_page.currentPage++
                                ingredient_page.updatePage()
                        }
                    }
                }
            }
        }

        Item {

            Layout.fillHeight: true
            Layout.fillWidth: true

            ListModel {
                id: ingredientModel
                onCountChanged: updatePage()
            }

            ListModel { id: pageModel }

            GridView {
                id: ingredientGrid

                anchors.fill: parent

                cellHeight: width * 0.15 + 35
                cellWidth: width / 4
                

                model: pageModel

                delegate: Item {
                    width: ingredientGrid.cellWidth
                    height: ingredientGrid.cellHeight

                    IngredientCard {
                        anchors.fill: parent
                        anchors.margins: ingredient_page.width * 0.007
                        anchors.bottomMargin: ingredient_page.width * 0.015


                        ingredient_name: name
                        category: category
                        n_recipes: n_recipes
                        total_price: total_price
                        price_unit: price_unit
                        total_weight: total_weight
                        weight_unit: weight_unit
                    }
                }
            }
        }

        Item {Layout.fillHeight: true}

    }
}
