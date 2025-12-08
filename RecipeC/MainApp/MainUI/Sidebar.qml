import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 2.15
import "ReusableComponents"

//Sidebar.qml

Rectangle {
    id: sidebar

    property string currentPage: ""
    signal pageSelected(string pagePath)

    anchors.top: parent.top
    anchors.bottom: parent.bottom
    anchors.left: parent.left
    width: parent.width * 0.13

    color: Theme.sidebar_bg_dark

    ColumnLayout {
        id: nav_column
        
        anchors.fill: parent
        spacing: sidebar.height * 0.018

        Item {
            Layout.preferredHeight: parent.height * 0.018
        }

        Item {
            Layout.fillWidth: true
            Layout.preferredHeight: sidebar.height * 0.025

            Text {
                anchors.left: parent.left
                anchors.leftMargin: parent.width * 0.1
                anchors.verticalCenter: parent.verticalCenter
                text: "Cake MD"
                font.bold: true

                color: Theme.background
                font.family: Theme.font_family
                font.pointSize: Theme.font_size_heading * font_scale
            }
        }

        Item {
            Layout.preferredHeight: sidebar.height * 0.025
        }
        
        SidebarButton {
            label: "Home"
            pageName: "Pages/Home.qml"
            Layout.fillWidth: true
            Layout.preferredHeight: sidebar.height * 0.05
        }

        SidebarButton {
            label: "Ingredients"
            pageName: "Pages/IngredientPage.qml"
            Layout.fillWidth: true
            Layout.preferredHeight: sidebar.height * 0.05
        }

        SidebarButton {
            label: "Recipes"
            pageName: "Pages/RecipePage.qml"
            Layout.fillWidth: true
            Layout.preferredHeight: sidebar.height * 0.05
        }

        SidebarButton {
            label: "Sales"
            pageName: "Pages/SalesPage.qml"
            Layout.fillWidth: true
            Layout.preferredHeight: sidebar.height * 0.05
        }

        SidebarButton {
            label: "Stock"
            pageName: "Pages/StockPage.qml"
            Layout.fillWidth: true
            Layout.preferredHeight: sidebar.height * 0.05
        }

        Item {
            Layout.fillHeight: true
        }

        SidebarButton {
            label: "Settings"
            pageName: "Pages/SettingsPage.qml"
            Layout.fillWidth: true
            Layout.preferredHeight: sidebar.height * 0.05
        }        

        Item {
            Layout.preferredHeight: sidebar.height * 0.005
        }
    }    
}