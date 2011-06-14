import QtQuick 1.0

import "/usr/share/mandriva/qt-components/desktop/components"
import "/usr/share/mandriva/qt-components/desktop/components/plugin"

Rectangle {

    SystemPalette {
        id: palette
        colorGroup: SystemPalette.Active
    }

    id: window
    width: 640
    height: 480
    color: palette.window

    ListModel {
        id: shellChoices
        ListElement { text: "/bin/bash" }
        ListElement { text: "/bin/dash" }
        ListElement { text: "/bin/sh" }
    }

    /** Header ****************************************************************/
    Rectangle {
        id: header
        width: window.width
        height: 50
        color: palette.window

        Row {
            anchors.verticalCenter: parent.verticalCenter
            anchors.left: parent.left
            anchors.leftMargin: 6
            spacing: 12

            Row {
                anchors.verticalCenter: parent.verticalCenter

                Button {
                    text: qsTr("Users")
                    onClicked: {
                        scrollFormGroup.state = ""
                        tab.currentIndex = 0
                    }
                }

                Button {
                    text: qsTr("Groups")
                    onClicked: {
                        scrollFormUser.state = ""
                        tab.currentIndex = 1
                    }
                }
            }

            Row {
                anchors.verticalCenter: parent.verticalCenter

                Button {
                    text: qsTr("Add user")
                    onClicked: {
                        tab.currentIndex = 0
                        scrollFormUser.state = "show"
                            editFormUser.visible = false
                        addFormUser.visible = true
                        scrollFormGroup.state = ""
                    }
                }

                Button {
                    text: qsTr("Add group")
                    onClicked: {
                        tab.currentIndex = 1
                        scrollFormGroup.state = "show"
                        scrollFormUser.state = ""
                        editGroupForm.visible = false
                        addGroupForm.visible = true
                    }
                }
            }
        }
    }

    VisualItemModel {
        id: tabModel

        /** User tab **********************************************************/
        Rectangle {
            id: userTab
            width: tab.width
            height: tab.height
            color: palette.alternateBase

            Component {
                id: userDelegate

                Item {
                    width: userGridView.cellWidth
                    height: userGridView.cellHeight

                    Column {
                        anchors.fill: parent
                        anchors.topMargin: 6

                        Image {
                            id: photo
                            source: status == Image.Error ? "/usr/share/faces/default.png" : "/usr/share/faces/" + model.user.userName + ".png"
                            anchors.horizontalCenter: parent.horizontalCenter
                            sourceSize.width: 96
                            sourceSize.height: 96
                        }

                        Text {
                            objectName: "delegateUserName"
                            text: model.user.userName
                            color: palette.text
                            width: 96
                            elide: Text.ElideRight
                            font.bold: true
                            horizontalAlignment: Text.Center
                        }
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            userGridView.currentIndex = index
                            scrollFormUser.state = "show"

                            fullName.text = model.user.fullName
                            userName.text = model.user.userName
                            loginShell.text = model.user.loginShell
                            homeDirectory.text = model.user.homeDirectory
                            shadowExpire.checked = model.user.shadowExpire
                            expirationDate.text = model.user.expirationDate
                            blockAccount.checked = model.user.isLocked
                            shadowMin.text = model.user.shadowMin
                            shadowMax.text = model.user.shadowMax
                            shadowWarning.text = model.user.shadowWarning
                            shadowInactive.text = model.user.shadowInactive
                            shadowLastChange.text = model.user.shadowLastChange

                            // Pass group members to systemUserModel internaly
                            systemGroupGridView.model.selectGroups(model.user.groups)

                            addFormUser.visible = false
                            editFormUser.visible = true
                        }
                    }
                }
            }

            GridView {
                id: userGridView
                cellWidth: 106
                cellHeight:128
                anchors.fill: parent
                model: userModel
                delegate: userDelegate
            }

            Rectangle {
                id: scrollFormUser
                y: -height
                z: 10
                width: userTab.width - 100
                height: userTab.height - 50
                color: palette.base
                clip: true
                anchors.horizontalCenter: parent.horizontalCenter

                /** Edit form user ********************************************/
                Item {
                    id: editFormUser
                    width: scrollFormUser.width
                    height: scrollFormUser.height
                    visible: false
                    //clip: true

                    Flickable {
                        anchors.fill: parent
                        contentWidth: editFormUser.width
                        contentHeight: myCol.height + 150

                        Column {
                            id: myCol
                            anchors.top: parent.top
                            anchors.topMargin: 6
                            anchors.left: parent.left
                            anchors.leftMargin: 6
                            spacing: 6

                            Grid {
                                columns: 2
                                spacing: 6

                                Text {
                                    text: qsTr("User last changed password on")
                                    font.bold: true
                                    color: palette.text
                                }

                                Text {
                                    id: shadowLastChange
                                    text: ""
                                    font.bold: true
                                    color: palette.text
                                }

                                Text {
                                    text: qsTr("Full name")
                                    font.bold: true
                                    color: palette.text
                                }

                                TextField {
                                    id: fullName
                                    objectName: "fullName"
                                    height: 26
                                    text: ""
                                    KeyNavigation.tab: userName
                                }

                                Text {
                                    text: qsTr("User name")
                                    font.bold: true
                                    color: palette.text
                                }

                                TextField {
                                    id: userName
                                    objectName: "userName"
                                    height: 26
                                    text: ""
                                    KeyNavigation.tab: password
                                }

                                Text {
                                    text: qsTr("Password")
                                    font.bold: true
                                    color: palette.text
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
                                    color: palette.text
                                }

                                TextField {
                                    id: confirmPassword
                                    objectName: "confirmPassword"
                                    height: 26
                                    text: ""
                                    echoMode: TextInput.Password
                                    KeyNavigation.tab: loginShell
                                }

                                Text {
                                    text: qsTr("Login shell")
                                    font.bold: true
                                    color: palette.text
                                }

                                TextField {
                                    id: loginShell
                                    objectName: "loginShell"
                                    height: 26
                                    text: ""
                                    KeyNavigation.tab: homeDirectory
                                }

                                Text {
                                    text: qsTr("Home directory")
                                    font.bold: true
                                    color: palette.text
                                }

                                TextField {
                                    id: homeDirectory
                                    objectName: "homeDirectory"
                                    height: 26
                                    text: ""
                                    KeyNavigation.tab: shadowExpire
                                }

                                Text {
                                    text: " "
                                }

                                CheckBox {
                                    id: shadowExpire
                                    objectName: "shadowExpire"
                                    text: qsTr("Enable account expiration")
                                    checked: false
                                    width: 200
                                    onCheckedChanged: !checked ? expirationDate.opacity = 0.6: expirationDate.opacity = 1
                                    KeyNavigation.tab: expirationDate
                                }

                                Text {
                                    text: qsTr("Account expires")
                                    font.bold: true
                                    color: palette.text
                                }

                                TextField {
                                    id: expirationDate
                                    objectName: "expirationDate"
                                    height: 26
                                    text: ""
                                    opacity: 0.6
                                    enabled: shadowExpire.checked
                                    KeyNavigation.tab: blockAccount
                                }

                                Text {
                                    text: " "
                                }

                                CheckBox {
                                    id: blockAccount
                                    objectName: "blockAccount"
                                    text: qsTr("Lock user account")
                                    checked: false
                                    width: 150
                                    KeyNavigation.tab: shadowMin
                                }

                                Text {
                                    text: qsTr("Days before change allowed")
                                    font.bold: true
                                    color: palette.text
                                }

                                TextField {
                                    id: shadowMin
                                    objectName: "shadowMin"
                                    height: 26
                                    text: ""
                                    KeyNavigation.tab: shadowMax
                                }

                                Text {
                                    text: qsTr("Days before change required")
                                    font.bold: true
                                    color: palette.text
                                }

                                TextField {
                                    id: shadowMax
                                    objectName: "shadowMax"
                                    height: 26
                                    text: ""
                                    KeyNavigation.tab: shadowWarning
                                }

                                Text {
                                    text: qsTr("Days warning before change")
                                    font.bold: true
                                    color: palette.text
                                }

                                TextField {
                                    id: shadowWarning
                                    objectName: "shadowWarning"
                                    height: 26
                                    text: ""
                                    KeyNavigation.tab: shadowInactive
                                }

                                Text {
                                    text: qsTr("Days before account inactive")
                                    font.bold: true
                                    color: palette.text
                                }

                                TextField {
                                    id: shadowInactive
                                    objectName: "shadowInactive"
                                    height: 26
                                    text: ""
                                }
                            }


                            Text {
                                text: qsTr("Select the groups that the user will be a member of")
                                font.bold: true
                                color: palette.text
                            }

                            Component {
                                id: systemGroupDelegate

                                Rectangle {
                                    width: 108
                                    height: 25
                                    color: ((index % 2 == 0) ? "#808080": "#999999")

                                    Row {
                                        spacing: 4
                                        anchors.left: parent.left
                                        anchors.leftMargin: 4

                                        Text {
                                            //id: checkbox
                                            text: "✔"
                                            font.pixelSize: 18
                                            font.bold: true
                                            opacity: ((model.group.isChecked) ? 1.0 : 0.1)
                                            color: "white"
                                            //anchors.verticalCenter: parent.verticalCenter
                                        }

                                        Text {
                                            text: model.group.groupName
                                            anchors.verticalCenter: parent.verticalCenter
                                            color: palette.text
                                        }
                                    }

                                    MouseArea {
                                        anchors.fill: parent
                                        onClicked: {
                                        controller.toggledGroup(systemGroupModel, model.group)
                                        }
                                    }
                                }
                            }

                            GridView {
                               id: systemGroupGridView
                               clip: true
                               height: 210 + 90
                               width: scrollFormUser.width
                               cellWidth: 108
                               cellHeight: 25
                               model: systemGroupModel
                               delegate: systemGroupDelegate
                            }
                        }
                    }

                    Rectangle {
                        height: 42
                        width: addFormUser.width
                        anchors.bottom: parent.bottom
                        anchors.right: parent.right
                        color: palette.base

                        Button {
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.left: parent.left
                            anchors.leftMargin: 6
                            text: qsTr("Delete")
                            //width: 60
                            //height: 30
                            onClicked: {
                                scrollFormUser.state = ""
                                controller.deleteUser(userModel, userGridView.currentItem, userGridView.currentIndex)
                            }
                        }

                        Row {
                            spacing: 12
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.right: parent.right
                            anchors.rightMargin: 6

                            Button {
                                text: qsTr("Save")
                                //width: 60
                                //height: 30
                                onClicked: {
                                    scrollFormUser.state = ""
                                    controller.modifyUser(userModel, editFormUser, userGridView.currentIndex)
                                }
                            }

                            Button {
                                text: qsTr("Close")
                                //width: 60
                                //height: 30
                                onClicked: scrollFormUser.state = ""
                            }
                        }
                    }
                }

                /** User add form ********************************************/
                Item {
                    id: addFormUser
                    width: scrollFormUser.width
                    height: scrollFormUser.height
                    visible: false
                    //clip: true

                    Flickable {
                        anchors.fill: parent
                        contentWidth: addFormUser.width
                        contentHeight: myGrid.height + 150

                        Grid {
                            id: myGrid
                            anchors.top: parent.top
                            anchors.topMargin: 6
                            anchors.left: parent.left
                            anchors.leftMargin: 6
                            columns: 2
                            spacing: 8

                            Text {
                                text: qsTr("Full name")
                                font.bold: true
                                color: palette.text
                            }

                            TextField {
                                id: fullNameAddForm
                                objectName: "fullNameAddForm"
                                height: 26
                                text: ""
                                KeyNavigation.tab: userNameAddForm
                            }

                            Text {
                                text: qsTr("User name")
                                font.bold: true
                                color: palette.text
                            }

                            TextField {
                                id: userNameAddForm
                                objectName: "userNameAddForm"
                                height: 26
                                text: ""
                                onTextChanged: homeDirectoryAddForm.text = "/home/" + text
                                KeyNavigation.tab: passwordAddForm
                            }

                            Text {
                                text: qsTr("Password")
                                font.bold: true
                                color: palette.text
                            }

                            TextField {
                                id: passwordAddForm
                                objectName: "passwordAddForm"
                                height: 26
                                text: ""
                                echoMode: TextInput.Password
                                KeyNavigation.tab: confirmPasswordAddForm
                            }

                            Text {
                                text: qsTr("Confirm password")
                                font.bold: true
                                color: palette.text
                            }

                            TextField {
                                id: confirmPasswordAddForm
                                objectName: "confirmPasswordAddForm"
                                height: 26
                                text: ""
                                echoMode: TextInput.Password
                                KeyNavigation.tab: loginShellAddForm
                            }

                            Text {
                                text: qsTr("Login shell")
                                font.bold: true
                                color: palette.text
                            }

                            /**
                            ChoiceList {
                                id: loginShellAddForm
                                objectName: "loginShellAddForm"
                                width: 200
                                focus: false
                                model: shellModel
                                KeyNavigation.tab: createHomeDirectoryAddForm
                            }
                            **/

                            TextField {
                                id: loginShellAddForm
                                objectName: "loginShellAddForm"
                                height: 26
                                text: "/bin/bash"
                                KeyNavigation.tab: createHomeDirectoryAddForm
                            }

                            Text {
                                text: " "
                            }

                            CheckBox {
                                id: createHomeDirectoryAddForm
                                objectName: "createHomeDirectoryAddForm"
                                text: qsTr("Create home directory")
                                checked: true
                                width: 200
                                KeyNavigation.tab: homeDirectoryAddForm
                            }

                            Text {
                                text: qsTr("Home directory")
                                font.bold: true
                                color: palette.text
                            }

                            TextField {
                                id: homeDirectoryAddForm
                                objectName: "homeDirectoryAddForm"
                                height: 26
                                text: "/home/"
                                KeyNavigation.tab: createPrivateGroupAddForm
                            }

                            Text {
                                text: " "
                            }

                            CheckBox {
                                id: createPrivateGroupAddForm
                                objectName: "createPrivateGroupAddForm"
                                text: qsTr("Create a private group for the user")
                                checked: true
                                width: 250
                                KeyNavigation.tab: specifyUserIdAddForm
                            }

                            Text {
                                text: " "
                            }

                            CheckBox {
                                id: specifyUserIdAddForm
                                objectName: "specifyUserIdAddForm"
                                text: qsTr("Specify user ID manually")
                                checked: false
                                width: 250
                                onCheckedChanged: !checked ? userIdAddForm.opacity = 0.6: userIdAddForm.opacity = 1
                                KeyNavigation.tab: userIdAddForm
                            }

                            Text {
                                text: qsTr("User ID")
                                font.bold: true
                                color: palette.text
                            }

                            TextField {
                                id: userIdAddForm
                                objectName: "userIdAddForm"
                                height: 26
                                text: ""
                                opacity: 0.6
                                enabled: specifyUserIdAddForm.checked
                            }
                        }
                    }

                    Rectangle {
                        height: 42
                        width: addFormUser.width
                        anchors.bottom: parent.bottom
                        anchors.right: parent.right
                        color: palette.base

                        Row {
                            spacing: 12
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.right: parent.right
                            anchors.rightMargin: 6

                            Button {
                                text: qsTr("Save")
                                //width: 60
                                //height: 30
                                onClicked: {
                                    scrollFormUser.state = ""
                                    // We pass groupModel here to be used to add a private group
                                    controller.addUser(userModel, addFormUser, groupModel)
                                }
                            }

                            Button {
                                text: qsTr("Close")
                                //width: 60
                                //height: 30
                                onClicked: scrollFormUser.state = ""
                            }
                        }
                    }
                }

                states : State {
                    name: "show"
                    PropertyChanges { target: scrollFormUser; y: 0}
                }

                transitions: Transition {
                    NumberAnimation { properties: "y"; duration: 500 }
                }
            }
        }

        /** Group tab *********************************************************/
        Rectangle {
            id: groupTab
            width: tab.width
            height: tab.height
            color: palette.alternateBase

            Component {
                id: groupDelegate

                Item {
                    height: 40
                    width: groupTab.width

                    Row {
                        spacing: 0
                        children: [

                            Item {
                                width: 50
                                height: 40

                                Text {
                                    text: model.group.gid
                                    elide: Text.ElideRight
                                    color: palette.text
                                    anchors.centerIn: parent
                                }
                            },

                            Text {
                                objectName: "delegateGroupName"
                                text: model.group.groupName
                                width: 150
                                elide: Text.ElideRight
                                font.bold: true
                                color: palette.text
                                anchors.verticalCenter: parent.verticalCenter
                            },

                            Text {
                                text: model.group.strMembers
                                width: 440
                                elide: Text.ElideRight
                                color: palette.text
                                anchors.verticalCenter: parent.verticalCenter
                            }
                        ]
                    }

                    MouseArea {
                        anchors.fill: parent
                        onClicked: {
                            groupListView.currentIndex = index
                            scrollFormGroup.state = "show"
                            groupName.text = model.group.groupName
                            // Pass group members to systemUserModel internaly
                            systemUserGridView.model.selectUsers(model.group.members)
                            addGroupForm.visible = false
                            editGroupForm.visible = true
                        }
                    }
                }
            }

            Component {
                id: highlightServices

                Rectangle {
                    width: groupTab.width
                    height: 40
                    color: palette.highlight
                    y: groupListView.currentItem.y;
                    Behavior on y { SpringAnimation { spring: 2; damping: 0.4 } }
                }
            }

            Component {
                id: headerDelegate

                Row {
                    spacing: 0
                    children: [

                        QStyleItem {
                            elementType: "header"
                            raised: true
                            width: 50
                            height: 30
                            text: qsTr("ID")
                        },

                        QStyleItem {
                            elementType: "header"
                            raised: true
                            width: 150 //(content.width - 50) / 2
                            height: 30
                            text: qsTr("Group name")
                        },

                        QStyleItem {
                            elementType: "header"
                            raised: true
                            width: 440 //(content.width - 50) / 2
                            height: 30
                            text: qsTr("Members")
                        }
                    ]
                }
            }

            ListView {
                id: groupListView
                anchors.fill: parent
                model: groupModel
                delegate: groupDelegate
                highlight: highlightServices
                highlightFollowsCurrentItem: false
                header: headerDelegate
            }

            Rectangle {
                id: scrollFormGroup
                y: -height
                z: 10
                color: palette.base
                width: groupTab.width - 100
                height: groupTab.height - 50
                clip: true
                anchors.horizontalCenter: parent.horizontalCenter

                /** Group edit form *******************************************/
                Item {
                    id: editGroupForm
                    width: scrollFormGroup.width
                    height: scrollFormGroup.height
                    visible: false

                    Flickable {
                        anchors.fill: parent
                        contentWidth: editGroupForm.width
                        contentHeight: groupColumn.height + 50

                        Column {
                            id: groupColumn
                            anchors.top: parent.top
                            anchors.topMargin: 6
                            anchors.left: parent.left
                            anchors.leftMargin: 6
                            spacing: 6

                            Grid {
                                columns: 2
                                spacing: 6

                                Text {
                                    text: qsTr("Group name")
                                    font.bold: true
                                    color: palette.text
                                }

                                TextField {
                                    id: groupName
                                    objectName: "groupName"
                                    height: 26
                                    text: ""
                                }
                            }

                            Text {
                                text: qsTr("Select the user to join this group")
                                font.bold: true
                                color: palette.text
                            }

                            Component {
                                id: systemUserDelegate

                                Rectangle {
                                    width: 108
                                    height: 25
                                    color: ((index % 2 == 0) ? "#808080": "#999999")

                                    Row {
                                        spacing: 4
                                        anchors.left: parent.left
                                        anchors.leftMargin: 4

                                        Text {
                                            //id: checkbox
                                            text: "✔"
                                            font.pixelSize: 18
                                            font.bold: true
                                            opacity: ((model.user.isChecked) ? 1.0 : 0.1)
                                            color: "white"
                                            //anchors.verticalCenter: parent.verticalCenter
                                        }

                                        Text {
                                            text: model.user.userName
                                            anchors.verticalCenter: parent.verticalCenter
                                            color: palette.text
                                        }
                                    }

                                    MouseArea {
                                        anchors.fill: parent
                                        onClicked: {
                                            controller.toggledUser(systemUserModel, model.user)
                                        }
                                    }
                                }
                            }

                            GridView {
                               id: systemUserGridView
                               clip: true
                               height: 210
                               width: scrollFormGroup.width
                               cellWidth: 108
                               cellHeight: 25
                               model: systemUserModel
                               delegate: systemUserDelegate
                            }
                        }
                    }

                    Rectangle {
                        height: 42
                        width: editGroupForm.width
                        anchors.bottom: parent.bottom
                        anchors.right: parent.right
                        color: palette.base

                        Button {
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.left: parent.left
                            anchors.leftMargin: 6
                            text: qsTr("Delete")
                            //width: 60
                            //height: 30
                            onClicked: {
                                scrollFormGroup.state = ""
                                controller.deleteGroup(groupModel, groupListView.currentItem, groupListView.currentIndex)
                            }
                        }

                        Row {
                            spacing: 12
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.right: parent.right
                            anchors.rightMargin: 6

                            Button {
                                text: qsTr("Save")
                                //width: 60
                                //height: 30
                                onClicked: {
                                    scrollFormGroup.state = ""
                                    controller.modifyGroup(groupModel, systemUserModel, editGroupForm, groupListView.currentIndex)
                                }
                            }

                            Button {
                                text: qsTr("Close")
                                //width: 60
                                //height: 30
                                onClicked: scrollFormGroup.state = ""
                            }
                        }
                    }
                }

                /** Group add form ********************************************/
                Item {
                    id: addGroupForm
                    width: scrollFormGroup.width
                    height: scrollFormGroup.height
                    visible: false

                    Flickable {
                        anchors.fill: parent
                        contentWidth: addGroupForm.width
                        contentHeight: groupGrid.height + 50

                        Grid {
                            id: groupGrid
                            anchors.top: parent.top
                            anchors.topMargin: 6
                            anchors.left: parent.left
                            anchors.leftMargin: 6
                            columns: 2
                            spacing: 6

                            Text {
                                text: qsTr("Group name")
                                font.bold: true
                                color: palette.text
                            }

                            TextField {
                                id: groupNameAddForm
                                objectName: "groupNameAddForm"
                                height: 26
                                text: ""
                                KeyNavigation.tab: specifyGidAddForm
                            }

                            Text {
                                text: " "
                            }

                            CheckBox {
                                id: specifyGidAddForm
                                objectName: "specifyGidAddForm"
                                text: qsTr("Specify group ID manually")
                                checked: false
                                width: 300
                                onCheckedChanged: !checked ? groupIdAddForm.opacity = 0.6: groupIdAddForm.opacity = 1
                                KeyNavigation.tab: groupIdAddForm
                            }

                            Text {
                                text: qsTr("Group Id")
                                font.bold: true
                                color: palette.text
                            }

                            TextField {
                                id: groupIdAddForm
                                objectName: "groupIdAddForm"
                                height: 26
                                text: ""
                                opacity: 0.6
                                enabled: specifyGidAddForm.checked
                            }
                        }
                    }

                    Rectangle {
                        height: 42
                        width: addFormUser.width
                        anchors.bottom: parent.bottom
                        anchors.right: parent.right
                        color: palette.base

                        Row {
                            spacing: 12
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.right: parent.right
                            anchors.rightMargin: 6

                            Button {
                                text: qsTr("Save")
                                //width: 60
                                //height: 30
                                onClicked: {
                                    scrollFormGroup.state = ""
                                    controller.addGroup(groupModel, addGroupForm)
                                }
                            }

                            Button {
                                text: qsTr("Close")
                                //width: 60
                                //height: 30
                                onClicked: scrollFormGroup.state = ""
                            }
                        }
                    }
                }

                states : State {
                    name: "show"
                    PropertyChanges { target: scrollFormGroup; y: 0}
                }

                transitions: Transition {
                    NumberAnimation { properties: "y"; duration: 500 }
                }
            }
        }
    }

    ListView {
        id: tab
        clip: true
        y: header.height
        height: window.height - header.height
        width: window.width
        model: tabModel
        preferredHighlightBegin: 0
        preferredHighlightEnd: 0
        highlightRangeMode: ListView.StrictlyEnforceRange
        orientation: ListView.Horizontal
        snapMode: ListView.SnapOneItem
    }
}
