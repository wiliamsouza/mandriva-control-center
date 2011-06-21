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
                    height: 25
                    onClicked: {
                        editGroupForm.visible = false
                        addGroupForm.visible = false
                        editFormUser.visible = false
                        addFormUser.visible = false
                        tab.currentIndex = 0
                    }
                }

                Button {
                    text: qsTr("Groups")
                    height: 25
                    onClicked: {
                        editGroupForm.visible = false
                        addGroupForm.visible = false
                        editFormUser.visible = false
                        addFormUser.visible = false
                        tab.currentIndex = 1
                    }
                }
            }

            Row {
                anchors.verticalCenter: parent.verticalCenter

                Button {
                    text: qsTr("Add user")
                    height: 25
                    onClicked: {
                        tab.currentIndex = 0
                        editGroupForm.visible = false
                        addGroupForm.visible = false
                        editFormUser.visible = false
                        addFormUser.visible = true
                    }
                }

                Button {
                    text: qsTr("Add group")
                    height: 25
                    onClicked: {
                        tab.currentIndex = 1
                        editFormUser.visible = false
                        addFormUser.visible = false
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
                            editUserFromScrollbar.value = 0
                            editUserFromFlick.contentY = 0
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

            /** User add form ********************************************/
            Rectangle {
                id: addFormUser
                width: addUserFromColumn.width + (addUserFromColumn.spacing * 2)
                height: addUserFromColumn.height + (addUserFromColumn.spacing * 2)
                anchors.centerIn: parent
                visible: false
                color: palette.base
                border.color: palette.shadow

                Column {
                    id: addUserFromColumn
                    spacing: 12
                    anchors.centerIn: parent

                    Grid {
                        id: myGrid
                        columns: 2
                        spacing: 12

                        Text {
                            text: qsTr("Full name")
                            font.bold: true
                            color: palette.text
                        }

                        TextField {
                            id: fullNameAddForm
                            objectName: "fullNameAddForm"
                            height: 27
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
                            height: 27
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
                            height: 27
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
                            height: 27
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
                            height: 27
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
                            height: 27
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
                            height: 27
                            text: ""
                            enabled: specifyUserIdAddForm.checked
                        }
                    }

                    Row {
                        spacing: 6
                        anchors.right: parent.right

                        Button {
                            text: qsTr("Save")
                            height: 25
                            onClicked: {
                                addFormUser.visible = false
                                // We pass groupModel here to be used to add a private group
                                controller.addUser(userModel, addFormUser, groupModel)
                            }
                        }

                        Button {
                            text: qsTr("Close")
                            height: 25
                            onClicked: addFormUser.visible = false
                        }
                    }
                }
            }

            /** Edit form user ********************************************/
            Rectangle {
                id: editFormUser
                width: editUserFromRow.width + 12
                height: tab.height - 50
                visible: false
                anchors.centerIn: parent
                color: palette.base
                border.color: palette.shadow
                clip: true

                Row {
                    id: editUserFromRow
                    anchors.left: parent.left
                    anchors.leftMargin: 12
                    anchors.top: parent.top
                    anchors.topMargin: 12
                    anchors.bottom: parent.bottom
                    anchors.bottomMargin: 12

                    Flickable {
                        id: editUserFromFlick
                        width: editUserFromColumn.width
                        height: editFormUser.height
                        contentWidth: editUserFromColumn.width
                        contentHeight: editUserFromColumn.height
                        onContentYChanged:  {
                            editUserFromScrollbar.value = editUserFromFlick.contentY
                        }

                        Column {
                            id: editUserFromColumn
                            spacing: 12

                            Column {
                                id: editUserFromColumn2
                                spacing: 12

                                Grid {
                                    columns: 2
                                    spacing: 12

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
                                        height: 27
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
                                        height: 27
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
                                        height: 27
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
                                        height: 27
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
                                        height: 27
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
                                        height: 27
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
                                        height: 27
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
                                        height: 27
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
                                        height: 27
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
                                        height: 27
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
                                        height: 27
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
                                        width: 115
                                        height: 25
                                        color: ((index % 2 == 0) ? "#808080": "#999999")

                                        Row {
                                            spacing: 4
                                            anchors.left: parent.left
                                            anchors.leftMargin: 4

                                            Text {
                                                text: "✔"
                                                font.pixelSize: 18
                                                font.bold: true
                                                opacity: ((model.group.isChecked) ? 1.0 : 0.1)
                                                color: "white"
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

                                Row {

                                    ScrollBar {
                                        id: editGroupFromGridViewScrollbar
                                        property int availableHeight : systemGroupGridView.height
                                        height: systemGroupGridView.height
                                        visible: systemGroupGridView.contentHeight > availableHeight
                                        orientation: Qt.Vertical
                                        maximumValue: systemGroupGridView.contentHeight > availableHeight ? systemGroupGridView.contentHeight - availableHeight : 0
                                        minimumValue: 0
                                        onValueChanged: {
                                            systemGroupGridView.contentY = value
                                        }
                                    }

                                    GridView {
                                        id: systemGroupGridView
                                        clip: true
                                        height: 300
                                        width: editUserFromColumn.width
                                        cellWidth: 115
                                        cellHeight: 25
                                        model: systemGroupModel
                                        delegate: systemGroupDelegate
                                        onContentYChanged:  {
                                            editGroupFromGridViewScrollbar.value = systemGroupGridView.contentY
                                        }
                                    }
                                }
                            }

                            Row {
                                spacing: 6
                                anchors.right: parent.right
                                anchors.rightMargin: 12

                                Button {
                                    text: qsTr("Delete")
                                    height: 25
                                    onClicked: {
                                        editFormUser.visible = false
                                        controller.deleteUser(userModel, userGridView.currentItem, userGridView.currentIndex)
                                    }
                                }

                                Button {
                                    text: qsTr("Save")
                                    height: 25
                                    onClicked: {
                                        editFormUser.visible = false
                                        controller.modifyUser(userModel, editFormUser, userGridView.currentIndex)
                                    }
                                }

                                Button {
                                    text: qsTr("Close")
                                    height: 25
                                    onClicked: editFormUser.visible = false
                                }
                            }
                        }
                    }

                    ScrollBar {
                        id: editUserFromScrollbar
                        property int availableHeight : editUserFromFlick.height - 24
                        height: editUserFromFlick.height - 24
                        visible: editUserFromFlick.contentHeight > availableHeight
                        orientation: Qt.Vertical
                        maximumValue: editUserFromFlick.contentHeight > availableHeight ? editUserFromFlick.contentHeight - availableHeight : 0
                        minimumValue: 0
                        onValueChanged: {
                            editUserFromFlick.contentY = value
                        }
                    }
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
                    id: groupItem
                    height: 40
                    width: groupTab.width

                    Row {
                        spacing: 0
                        children: [

                            Item {
                                id: gidItem
                                width: 50
                                height: groupItem.height

                                Text {
                                    text: model.group.gid
                                    elide: Text.ElideRight
                                    color: palette.text
                                    anchors.centerIn: parent
                                }
                            },

                            Text {
                                id: groupNameItem
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
                                width: groupItem.width - (groupNameItem.width - gidItem.width) //440
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
                            id: headerGid
                            elementType: "header"
                            raised: true
                            width: 50
                            height: 30
                            text: qsTr("GID")
                        },

                        QStyleItem {
                            id: headerGroupName
                            elementType: "header"
                            raised: true
                            width: 150
                            height: 30
                            text: qsTr("Group name")
                        },

                        QStyleItem {
                            elementType: "header"
                            raised: true
                            width: groupTab.width - (headerGroupName.width + headerGid.width)
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

            /** Add group form ********************************************/
            Rectangle {
                visible: false
                id: addGroupForm
                color: palette.base
                anchors.centerIn: parent
                border.color: palette.shadow
                width: addGroupFromColumn.width + (addGroupFromColumn.spacing * 2)
                height: addGroupFromColumn.height + (addGroupFromColumn.spacing * 2)

                Column {
                    id: addGroupFromColumn
                    spacing: 12
                    anchors.centerIn: parent

                    Grid {
                        columns: 2
                        spacing: 12

                        Text {
                            font.bold: true
                            color: palette.text
                            text: qsTr("Group name")
                        }

                        TextField {
                            id: groupNameAddForm
                            objectName: "groupNameAddForm"
                            height: 27
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
                            width: 200
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
                            height: 27
                            text: ""
                            opacity: 0.6
                            enabled: specifyGidAddForm.checked
                        }
                    }

                    Row {
                        id: addGroupFormButtons
                        anchors.right: parent.right
                        spacing: 6

                        Button {
                            text: qsTr("Save")
                            height: 25
                            onClicked: {
                                addGroupForm.visible = false
                                controller.addGroup(groupModel, addGroupForm)
                            }
                        }

                        Button {
                            text: qsTr("Close")
                            height: 25
                            onClicked: {
                                addGroupForm.visible = false
                            }
                        }
                    }
                }
            }

            /** Group edit form *******************************************/
            Rectangle {
                id: editGroupForm
                width: editGroupFromColumn.width + (editGroupFromColumn.spacing * 2)
                height: editGroupFromColumn.height + (editGroupFromColumn.spacing * 2)
                anchors.centerIn: parent
                visible: false
                color: palette.base
                border.color: palette.shadow

                Column {
                    id: editGroupFromColumn
                    anchors.centerIn: parent
                    spacing: 12

                    Column {
                        spacing: 12

                        Grid {
                            id: mygrid
                            columns: 2
                            spacing: 12

                            Text {
                                text: qsTr("Group name")
                                font.bold: true
                                color: palette.text
                            }

                            TextField {
                                id: groupName
                                objectName: "groupName"
                                height: 27
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
                                width: 100
                                height: 25
                                color: ((index % 2 == 0) ? "#808080": "#999999")

                                Row {

                                    Text {
                                        text: "✔"
                                        font.pixelSize: 18
                                        font.bold: true
                                        opacity: ((model.user.isChecked) ? 1.0 : 0.1)
                                        color: "white"
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

                        Row {

                            GridView {
                               id: systemUserGridView
                               clip: true
                               height: 225
                               width: 400
                               cellWidth: 100
                               cellHeight: 25
                               model: systemUserModel
                               delegate: systemUserDelegate
                               onContentYChanged:  {
                                   editGroupFromScrollbar.value = systemUserGridView.contentY
                               }
                            }

                            ScrollBar {
                                id: editGroupFromScrollbar
                                property int availableHeight : systemUserGridView.height
                                height: systemUserGridView.height
                                visible: systemUserGridView.contentHeight > availableHeight
                                orientation: Qt.Vertical
                                maximumValue: systemUserGridView.contentHeight > availableHeight ? systemUserGridView.contentHeight - availableHeight : 0
                                minimumValue: 0
                                onValueChanged: {
                                    systemUserGridView.contentY = value
                                }
                            }
                        }
                    }

                    Row {
                        spacing: 6
                        anchors.right: parent.right

                        Button {
                            text: qsTr("Delete")
                            height: 25
                            onClicked: {
                                editGroupForm.visible = false
                                controller.deleteGroup(groupModel, groupListView.currentItem, groupListView.currentIndex)
                            }
                        }

                        Button {
                            text: qsTr("Save")
                            height: 25
                            onClicked: {
                                editGroupForm.visible = false
                                controller.modifyGroup(groupModel, systemUserModel, editGroupForm, groupListView.currentIndex)
                            }
                        }

                        Button {
                            text: qsTr("Close")
                            height: 25
                            onClicked: {
                                editGroupForm.visible = false
                            }
                        }
                    }
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
