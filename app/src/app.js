import React from 'react'
import ReactDOM from 'react-dom'
import moment from 'moment'
import AyxStore from './stores/AyxStore'
import { extendObservable, autorun, toJS } from 'mobx'
//
// Alteryx.Gui.BeforeLoad = function(manager, AlteryxDataItems) {
//   // Manually create a new data item for the widget with the specified dataname.
//   const RadioURL = new AlteryxDataItems.StringSelector({dataName: 'RadioURL', id: 'dataItem1'})
//   // Set the list of selectable options for this data item.
//   RadioURL.StringList
//     .Add('URLField', 'Input URL From Field')
//     .Add('URLMan', 'Input URL Manually')
//   // Add this data item to the manager.
//   manager.AddDataItem(RadioURL)
//     // Set the value of the data item.
//   RadioURL.setValue('URLField')
// }
//
// Alteryx.Gui.AfterLoad = (manager) => {
//   const collection = [
//     {key: 'URLDrop', type: 'value'},
//     {key: 'URLText', type: 'value'}
//     // {key: 'RadioURL', type: 'RadioButton'}
//   ]
//
//   // Instantiate the mobx store which will sync all dataItems specified in the collection.
//   const store = new AyxStore(manager, collection)
//   extendObservable(store, {
//     get URL () {
//       const array = [
//         store.URLDrop,
//         store.URLText
//         // store.RadioURL
//       ]
//       return array
//     }
//   })
//
// // Because radio buttons for whatever reason default to the value simple, we change it to the value of URLField
//   autorun(() => {
//     if (store.RadioURL.value === 'simple') {
//       store.RadioURL.setValue('URLField')
//     }
//   })
//
// //  Hide/unhide URL field selector if radio button is selected
//   autorun(() => {
//     if (store.RadioURL === 'URLField') {
//       document.getElementById('urlDrop').style.display = 'block'
//       console.log(store.RadioURL)
//     } else {
//       document.getElementById('urlDrop').style.display = 'none'
//     }
//   })
//
// //  Hide/unhide URL textbox selector if radio button is selected
//   autorun(() => {
//     if (store.RadioURL === 'URLMan') {
//       document.getElementById('urlText').style.display = 'block'
//       console.log(store.RadioURL)
//     } else {
//       document.getElementById('urlText').style.display = 'none'
//     }
//   })
// }
// Used to show/hide different fielsets
const setPage = (fieldsetName) => {
  // Array containing all fieldsets
  let hideArray = [
    '#HTTP',
    '#Headers',
    '#Payload',
    '#Credentials'
  ]

  let showArray = []

  showArray.push(fieldsetName)

  $(document).ready(() => {
    // Hide each item in the hideArray
    hideArray.forEach((v) => {
      $(v).hide()
    })
    // Show the fieldset corresponding with fieldsetName
    showArray.forEach((v) => {
      $(v).show()
    })
  })
}

// Alteryx.Gui.AfterLoad = (manager) => {
//   // Used to show/hide different fielsets
//   displaySort()
//   Alteryx.Gui.Manager.getDataItem('DoSort').registerPropertyListener('value', displaySort)
// }
