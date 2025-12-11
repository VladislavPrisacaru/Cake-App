import QtQuick 2.15
import QtQuick.Controls 2.15
import "Pages"

//Main.qml

ApplicationWindow {
    id: mainWindow
    visible: true

    width: Screen.width    // full screen width
    height: Screen.height
    visibility: Window.Maximized
    color: Theme.background

    property real font_scale: mainWindow.width / 1920
    
    Row {
        anchors.fill: parent

        Sidebar {
            id: sidebar
            onPageSelected: pageManager.showPage(pageName)
        }

        Item {
            id: pageManager
            width: parent.width - sidebar.width
            height: parent.height

            // Function that switches pages
            function showPage(name) {
                homePage.visible = name === "Pages/Home.qml"
                ingredientPage.visible = name === "Pages/IngredientPage.qml"
                recipePage.visible = name === "Pages/RecipePage.qml"
                salesPage.visible = name === "Pages/SalesPage.qml"
                stockPage.visible = name === "Pages/StockPage.qml"
                settingsPage.visible = name === "Pages/SettingsPage.qml"
            }

            // All pages loaded once, stacked
            Home {
                id: homePage
                anchors.fill: parent
                visible: false
            }

            IngredientPage {
                id: ingredientPage
                anchors.fill: parent
                visible: false
            }

            RecipePage {
                id: recipePage
                anchors.fill: parent
                visible: false
            }

            SalesPage {
                id: salesPage
                anchors.fill: parent
                visible: false
            }

            StockPage {
                id: stockPage
                anchors.fill: parent
                visible: false
            }

            SettingsPage {
                id: settingsPage
                anchors.fill: parent
                visible: false
            }
        }
    }
}