import AyxStore from '../stores/AyxStore'

// Developer acccess_token request triggered by Connect button on developerCreds page
const devLogin = () => {
  const auth = store.client_id.trim() + ':' + store.client_secret.trim()

  var settings = {
    'async': true,
    'crossDomain': true,
    'url': 'https://api.omniture.com/token',
    'method': 'POST',
    'headers': {
      'authorization': 'Basic ' + btoa(auth),
      'content-type': 'application/x-www-form-urlencoded',
      'cache-control': 'no-cache'
    },
    'data': {
      'grant_type': 'client_credentials'
    }
  }

  $.ajax(settings)
    .done((data) => {
      store.access_token = data.access_token
      store.errorStatus = ''
      store.page === '#developerCreds' ? setPage('#reportSuite') : ''
    })
    .fail((jqXHR, textStatus, errorThrown) => {
      store.page = '#developerCreds'
      errorMessaging(jqXHR, textStatus, errorThrown)
      showLoader(false)
    })
}

// User access_token request triggered by User Login button on authSelect page
const userLogin = () => {
  const base = 'https://marketing.adobe.com/authorize?'
  const scope = 'Company ReportSuite Report'  // may need to add to this later
  const clientId = '3398773387-alteryx'
  const redirectUri = 'https://developers.google.com/oauthplayground'
  const _url = base + 'scope=' + scope + '&redirect_uri=' + redirectUri + '&response_type=token' + '&client_id=' + clientId + '&access_type=offline'
  const win = window.open(_url, 'windowname1', 'width=800, height=600')

  showLoader(true)
  store.errorStatus = ''

  const pollTimer = window.setInterval(() => {
    try {
      if (win.document.location.origin === 'https://developers.google.com') {
        const url = win.document.URL
        const accessToken = parseToken(url, 'access_token')
        store.access_token = accessToken
        win.close()
        showLoader(false)
        setPage('#reportSuite')
        clearInterval(pollTimer)
      }
    } catch (e) {
    }
  }, 500)

  const clearUserLoginInterval = setInterval(() => {
    if (win.closed && typeof store.acccess_token === 'undefined') {
      if (store.page !== '#reportSuite') {
        showLoader(false)
      }
      clearInterval(clearUserLoginInterval)
      clearInterval(pollTimer)
    }
  }, 500)
}

// Parses access_token from the response url returned in userLogin
const parseToken = (url, name) => {
  name = name.replace(/[\[]/, '\\\[').replace(/[\]]/, '\\\]')
  const regexS = '[\\#&]' + name + '=([^&#]*)'
  const regex = new RegExp(regexS)
  const results = regex.exec(url)
  if (results == null) {
    return ''
  } else {
    return results[1]
  }
}

const errorMessaging = (jqXHR, textStatus, errorThrown) => {
  showLoader(false)
  switch (jqXHR.responseJSON.error_description) {
    case 'XMSG("The access token provided has expired")':
      store.errorStatus = 1
      break
    case 'XMSG("The client credentials are invalid")':
      store.errorStatus = 401
      break
    default:
      store.errorStatus = jqXHR.status
  }
}

const setPage = (page) => {
  store.page = page
}

// Used to show/hide different fielsets
const displayFieldset = (fieldsetName) => {
  // Array containing all fieldsets
  let hideArray = [
    '#authSelect',
    '#developerCreds',
    '#datePickers',
    '#reportSuite',
    '#metricSelectors',
    '#elementSelectors',
    '#segmentSelectors',
    '#summary'
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

const showLoader = (flag) => {
  if (flag) {
    document.getElementById('loading').style.display = 'block'
    document.getElementById('loading-inner').innerHTML = '<p style="font-size: 14px">XMSG("Sign in to Adobe Analytics<br>using the popup")</p><img src=".//assets//loading_ring.svg">'
    document.getElementById('loading-inner').style.display = 'block'
  } else {
    document.getElementById('loading').style.display = 'none'
    document.getElementById('loading-inner').innerHTML = '<img src=".//assets//loading_ring.svg">'
    document.getElementById('loading-inner').style.display = 'none'
  }
}

const advOptionsToggle = (element) => {
  switch (element) {
    case 'primary':
      if (store.advOptionsPrimary === true) {
        document.getElementById('primaryArrow').className = 'arrow-right'
        store.advOptionsPrimary = false
      } else {
        document.getElementById('primaryArrow').className = 'arrow-down'
        store.advOptionsPrimary = true
      }
      break
    case 'secondary':
      if (store.advOptionsSecondary === true) {
        document.getElementById('secondaryArrow').className = 'arrow-right'
        store.advOptionsSecondary = false
      } else {
        document.getElementById('secondaryArrow').className = 'arrow-down'
        store.advOptionsSecondary = true
      }
      break
    case 'tertiary':
      if (store.advOptionsTertiary === true) {
        document.getElementById('tertiaryArrow').className = 'arrow-right'
        store.advOptionsTertiary = false
      } else {
        document.getElementById('tertiaryArrow').className = 'arrow-down'
        store.advOptionsTertiary = true
      }
      break
  }
}

const resetFields = () => {
  const valueArray = [
    'reportDescription',
    'client_id',
    'client_secret',
    'access_token',
    'errorStatus',
    'reportSuite',
    'metric1',
    'metric2',
    'metric3',
    'metric4',
    'metric5',
    'granularity',
    'elementPrimary',
    'elementSecondary',
    'elementTertiary',
    'elementPrimaryClassification',
    'elementSecondaryClassification',
    'elementTertiaryClassification',
    'segment1',
    'segment2',
    'segment3',
    'segment4',
    'segment5'
  ]

  // Resets the selection value for widgets
  valueArray.forEach((item) => {
    Alteryx.Gui.manager.GetDataItem(item).setValue('')
  })

  // reset record limit values to 100
  Alteryx.Gui.manager.GetDataItem('topPrimary').setValue(100)
  Alteryx.Gui.manager.GetDataItem('topSecondary').setValue(100)
  Alteryx.Gui.manager.GetDataItem('topTertiary').setValue(100)

  // reset starting with values to 1
  Alteryx.Gui.manager.GetDataItem('startingWithPrimary').setValue(1)
  Alteryx.Gui.manager.GetDataItem('startingWithSecondary').setValue(1)
  Alteryx.Gui.manager.GetDataItem('startingWithTertiary').setValue(1)

  // reset advanced option values to false
  Alteryx.Gui.manager.GetDataItem('advOptionsPrimary').setValue(false)
  Alteryx.Gui.manager.GetDataItem('advOptionsSecondary').setValue(false)
  Alteryx.Gui.manager.GetDataItem('advOptionsTertiary').setValue(false)

  // Set default value for preDefDropDown and advOptionsPrimary, advOptionsSecondary, advOptionsTertiary
  Alteryx.Gui.manager.GetDataItem('preDefDropDown').setValue('today')

  // set stringList of store.elementPrimary and store.segment1 to empty. This lets the autoruns of API calls to run as expected
  store.elementPrimary.stringList = []
  store.segment1.stringList = []
}

export { devLogin, userLogin, setPage, displayFieldset, resetFields, advOptionsToggle }
