/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/

import QtQuick 6.5
import QtQuick.Controls 6.5
import StreamingService

Rectangle {
    width: Constants.width
    height: Constants.height
    color: "#4a507e"


    Image {
        id: image
        x: 561
        y: -45
        width: 799
        height: 562
        source: "../../../Desktop/Logo (2).png"
        fillMode: Image.PreserveAspectFit
    }

    Column {
        id: column
        x: 859
        y: 384
        width: 310
        height: 400
        visible: true
        transformOrigin: Item.Center
        z: 0
        clip: false
        focus: false
        topPadding: 0
        spacing: 50

        TextInput {
            id: textInput
            width: 80
            height: 20
            opacity: 1
            color: "#ffffff"
            text: qsTr("Username")
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.leftMargin: 92
            anchors.topMargin: 25
            font.letterSpacing: 1
            font.pixelSize: 28
            horizontalAlignment: Text.AlignLeft
            font.styleName: "Black"
            font.bold: true
            clip: false
        }

        TextInput {
            id: textInput1
            width: 80
            height: 20
            color: "#ffffff"
            text: qsTr("Password")
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.leftMargin: 89
            anchors.topMargin: 75
            font.letterSpacing: 1
            font.pixelSize: 28
            font.styleName: "Black"
            echoMode: TextInput.Password
            font.italic: false
            font.bold: true
        }

        Button {
            id: button
            width: 200
            text: qsTr("Login")
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.leftMargin: 0
            anchors.topMargin: 125
            font.styleName: "Black"
            font.pointSize: 24
            font.family: "Arial"
            icon.width: 24
            icon.color: "#045ab1"
            highlighted: true
            flat: false
        }

        Button {
            id: button2
            width: 200
            text: qsTr("Register")
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.leftMargin: 0
            anchors.topMargin: 200
            font.styleName: "Black"
            icon.width: 24
            icon.color: "#045ab1"
            highlighted: true
            font.pointSize: 24
            font.family: "Arial"
            flat: false
        }

    }
}
