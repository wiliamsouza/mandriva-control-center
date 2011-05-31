import QtQuick 1.0

import "/usr/share/mandriva/qt-components/desktop/components"
import "/usr/share/mandriva/qt-components/desktop/components/plugin"

Rectangle {
    id: window
    width: 640
    height: 480
    color: "#4d4d4d"

    Rectangle {
        id: header
        width: window.width
        height: 100
        color: "#333333"

        Image {
            id: mandrivaLogo
            source: "images/mandriva_logo.png"
            anchors.left: parent.left
            anchors.leftMargin: 12
            anchors.verticalCenter: parent.verticalCenter
        }

        Row {
            anchors.right: parent.right
            anchors.rightMargin: 12
            anchors.bottom: parent.bottom
            anchors.bottomMargin: 12
            spacing: 12
            children: [
                Button {
                    text: "New"
                    onClicked: {
                        scrollForm.state = "show"
                        preferencesForm.visible = false
                        addBootForm.visible = true
                    }
                },
                Button {
                    text: "Preferences"
                    onClicked: {
                        scrollForm.state = "show"
                        addBootForm.visible = false
                        preferencesForm.visible = true
                    }
                }
            ]
        }
    }

    Rectangle {
        id: content
        y: header.height
        height: window.height - header.height
        width: window.width
        color: "#4d4d4d"
        clip: true

        ListModel {
            id: rootChoices
            ListElement { text: "/dev/sda1" }
            ListElement { text: "/dev/sda5" }
            ListElement { text: "/dev/sda6" }
        }

        ListModel {
            id: imageChoices
            ListElement { text: "/boot/vmlinuz" }
            ListElement { text: "/boot/vmlinuz-2.6.38.5-desktop-1mnb2" }
            ListElement { text: "/boot/vmlinuz-2.6.38.4-desktop-1mnb2" }
            ListElement { text: "/boot/vmlinuz-2.6.38.3-desktop-1mnb2" }
        }

        ListModel {
            id: videoChoices
            ListElement { text: "800x600 16bpp" }
            ListElement { text: "1024x768 16 bpp" }
            ListElement { text: "640x480 15 bpp" }
            ListElement { text: "1280x1024 8bpp" }
        }

        ListModel {
            id: bootloaderChoices
            ListElement { text: "Grub" }
            ListElement { text: "Lilo" }
        }

       Rectangle {
            id: scrollForm
            y: -height
            z: 10
            color: "#b3b3b3"
            width: content.width - 100
            height: content.height - 25
            clip: true
            anchors.horizontalCenter: parent.horizontalCenter

            Item {
                id: preferencesForm
                width: scrollForm.width
                height: scrollForm.height
                visible: false

                Flickable {
                    anchors.fill: parent
                    contentWidth: preferencesForm.width
                    contentHeight: bootColumn.height + 50

                    Column {
                        id: bootColumn
                        anchors.top: parent.top
                        anchors.topMargin: 6
                        anchors.left: parent.left
                        anchors.leftMargin: 6
                        spacing: 6

                        Grid {
                            columns: 2
                            spacing: 6

                            Text {
                                text: qsTr("Bootloader")
                                font.bold: true
                                opacity: 0.7
                            }

                            TextField {
                                height: 26
                                text: ""
                            }

                            /**
                            ChoiceList {
                                model: bootloaderChoices;
                                width: 200;
                                focus: false;
                            }
                            **/

                            Text {
                                text: qsTr("Boot device")
                                font.bold: true
                                opacity: 0.7
                            }

                            TextField {
                                height: 26
                                text: ""
                            }

                            /**
                            ChoiceList {
                                model: rootChoices;
                                width: 200;
                                focus: false;
                            }
                            **/

                            Text {
                                text: qsTr("Delay before booting default image")
                                font.bold: true
                                opacity: 0.7
                            }

                            TextField {
                                height: 26
                                text: ""
                            }

                            Text {
                                text: qsTr("Password")
                                font.bold: true
                                opacity: 0.7
                            }

                            TextField {
                                id: password
                                objectName: "password"
                                height: 26
                                text: ""
                                echoMode: TextInput.Password
                                KeyNavigation.tab: confirmPassword
                            }

                            Text {
                                text: qsTr("Confirm password")
                                font.bold: true
                                opacity: 0.7
                            }

                            TextField {
                                id: confirmPassword
                                objectName: "confirmPassword"
                                height: 26
                                text: ""
                                echoMode: TextInput.Password
                            }

                            CheckBox {
                                text: "Enable ACPI"
                                checked: false
                                width: 100
                            }

                            CheckBox {
                                text: "Enable SMP"
                                checked: false
                                width: 100
                            }

                            CheckBox {
                                text: "Enable APIC"
                                checked: false
                                width: 100
                            }

                            CheckBox {
                                text: "Enable local APIC"
                                checked: false
                                width: 100
                            }

                            CheckBox {
                                text: "Clean /tmp at each boot"
                                checked: false
                                width: 100
                            }
                        }
                    }
                }

                Rectangle {
                    height: 42
                    width: preferencesForm.width
                    anchors.bottom: parent.bottom
                    anchors.right: parent.right
                    color: "#333333"

                    Row {
                        spacing: 12
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.right: parent.right
                        anchors.rightMargin: 6

                        Button {
                            text: qsTr("Save")
                            onClicked: {
                                scrollForm.state = ""
                            }
                        }

                        Button {
                            text: qsTr("Close")
                            onClicked: scrollForm.state = ""
                        }
                    }
                }
            }

            Item {
                id: addBootForm
                width: scrollForm.width
                height: scrollForm.height
                visible: false

                Flickable {
                    anchors.fill: parent
                    contentWidth: addBootForm.width
                    contentHeight: bootGrid.height + 50

                    Grid {
                        id: bootGrid
                        anchors.top: parent.top
                        anchors.topMargin: 6
                        anchors.left: parent.left
                        anchors.leftMargin: 6
                        columns: 2
                        spacing: 6

                        CheckBox {
                            text: "Default"
                            checked: false
                        }

                        Text {
                            text: " "
                        }

                        Text {
                            text: qsTr("Wich type of entry do you want do add?")
                            font.bold: true
                            opacity: 0.7
                        }

                        Text {
                            text: " "
                        }

                        ButtonRow {

                            RadioButton {
                                id: linuxRadioButton
                                text: "GNU/Linux"
                                checked: true
                            }

                            RadioButton {
                                text: "Other OS"
                            }
                        }

                        Text {
                            text: " "
                        }

                        Text {
                            text: qsTr("Label")
                            font.bold: true
                            opacity: 0.7
                        }

                        TextField {
                            height: 26
                            text: ""
                        }

                        Text {
                            text: qsTr("Image")
                            font.bold: true
                            opacity: 0.7
                        }

                        TextField {
                            height: 26
                            text: ""
                            enabled: linuxRadioButton.checked
                        }

                        /**
                        ChoiceList {
                            model: imageChoices;
                            width: 200;
                            focus: false;
                            enabled: linuxRadioButton.checked
                        }
                        **/

                        Text {
                            text: qsTr("Root")
                            font.bold: true
                            opacity: 0.7
                        }

                        TextField {
                            height: 26
                            text: ""
                        }

                        /**
                        ChoiceList {
                            model: rootChoices;
                            width: 200;
                            focus: false;
                        }
                        **/

                        Text {
                            text: qsTr("Append")
                            font.bold: true
                            opacity: 0.7
                        }

                        TextField {
                            height: 26
                            text: ""
                            enabled: linuxRadioButton.checked
                        }


                        Text {
                            text: qsTr("Video Mode")
                            font.bold: true
                            opacity: 0.7
                        }

                        TextField {
                            height: 26
                            text: ""
                            enabled: linuxRadioButton.checked
                        }

                        /**
                        ChoiceList {
                            model: videoChoices;
                            width: 200;
                            focus: false;
                            enabled: linuxRadioButton.checked
                        }
                        **/

                        Text {
                            text: qsTr("Initrd")
                            font.bold: true
                            opacity: 0.7
                        }

                        TextField {
                            height: 26
                            text: ""
                            enabled: linuxRadioButton.checked
                        }

                        Text {
                            text: qsTr("Network profile")
                            font.bold: true
                            opacity: 0.7
                        }

                        TextField {
                            height: 26
                            text: ""
                            enabled: linuxRadioButton.checked
                        }
                    }
                }

                Rectangle {
                    height: 42
                    width: addBootForm.width
                    anchors.bottom: parent.bottom
                    anchors.right: parent.right
                    color: "#333333"

                    Row {
                        spacing: 12
                        anchors.verticalCenter: parent.verticalCenter
                        anchors.right: parent.right
                        anchors.rightMargin: 6

                        Button {
                            text: qsTr("Save")
                            onClicked: {
                                scrollForm.state = ""
                            }
                        }

                        Button {
                            text: qsTr("Close")
                            onClicked: scrollForm.state = ""
                        }
                    }
                }
            }

            states : State {
                name: "show"
                PropertyChanges { target: scrollForm; y: 0}
            }

            transitions: Transition {
                NumberAnimation { properties: "y"; duration: 500 }
            }
        }

        ListModel {
            id: bootListModel

            ListElement {
                name: "linux"
                image: "/boot/vmlinuz"
                root: "/dev/sda5"
                append: "nokmsboot splash=silent"
                videoMode: "800x600 16bpp"
                initrd: "/boot/initrd.img"
                networkProfile: ""
                isDefault: true
            }

            ListElement {
                name: "linux-nonfb"
                image: "/boot/vmlinuz"
                root: "/dev/sda5"
                append: "nokmsboot"
                videoMode: ""
                initrd: "/boot/initrd.img"
                networkProfile: ""
                isDefault: false
            }

            ListElement {
                name: "failsafe"
                image: "/boot/vmlinuz"
                root: "/dev/sda5"
                append: "nokmsboot failsafe"
                videoMode: ""
                initrd: "/boot/initrd.img"
                networkProfile: ""
                isDefault: false
            }

            ListElement {
                name: "ubuntu"
                image: "(hd0,0)/boot/grub/core.img"
                root: "/dev/sda1"
                append: ""
                videoMode: ""
                initrd: ""
                networkProfile: ""
                isDefault: false
            }

            ListElement {
                name: "2.6.38.4-desktop-1mnb2"
                image: "/boot/vmlinuz-2.6.38.4-desktop-1mnb2"
                root: "/dev/sda5"
                append: "nokmsboot splash=silent"
                videoMode: "800x600 16bpp"
                initrd: "/boot/initrd-2.6.38.4-desktop-1mnb2.img"
                networkProfile: ""
                isDefault: false
            }

            ListElement {
                name: "2.6.38.5-desktop-1mnb2"
                image: "/boot/vmlinuz-2.6.38.5-desktop-1mnb2"
                root: "/dev/sda5"
                append: "nokmsboot splash=silent"
                videoMode: "800x600 16bpp"
                initrd: "/boot/initrd-2.6.38.5-desktop-1mnb2.img"
                networkProfile: ""
                isDefault: false
            }
        }

        Component {
            id: bootDelegate

            Rectangle {
                width: content.width
                height: 30
                color: ((index % 2 == 0) ? "#808080": "#999999")
                clip: true

                Row {
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.top: parent.top
                    anchors.topMargin: 12
                    anchors.left: parent.left
                    anchors.leftMargin: 12
                    spacing: 6
                    children: [
                        /**
                        Text {
                            text: "✔"
                            font.pixelSize: 18
                            font.bold: true
                            opacity: ((model.isDefault) ? 1.0 : 0.1)
                            color: "white"
                        },
                        **/
                        Text {
                            width: content.width / 4
                            elide: Text.ElideRight
                            text: model.name
                            opacity: 0.7
                            font.bold: true
                        },

                        Text {
                            width: content.width / 4
                            elide: Text.ElideRight
                            text: model.image
                            opacity: 0.7
                        },

                        Text {
                            width: content.width / 4
                            elide: Text.ElideRight
                            text: model.root
                            opacity: 0.7
                        },

                        Text {
                            width: content.width / 4
                            elide: Text.ElideRight
                            text: model.initrd
                            opacity: 0.7
                        }
                    ]
                }
            }
        }

        ListView {
            id: bootListView
            anchors.fill: parent
            model: bootListModel
            delegate: bootDelegate
       }

    }
}
