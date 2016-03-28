angular.module('comment')

.config([
  '$mdThemingProvider', 
  function(
    $mdThemingProvider
  ){
    $mdThemingProvider.setDefaultTheme('bolt');
    $mdThemingProvider.definePalette('boltPrimaryPalette', {
      '50': 'ffebee',
      '100': 'ffcdd2',
      '200': 'ef9a9a',
      '300': 'e57373',
      '400': 'ef5350',
      '500': '7eae64',
      '600': '506e00',
      '700': 'fff',
      '800': 'fff',
      '900': 'fff',
      'A100': 'fff',
      'A200': 'fff',
      'A400': 'fff',
      'A700': 'fff',
      'contrastDefaultColor': 'light',
      'contrastDarkColors': ['50', '100', '200', '300', '400', 'A100'],
      'contrastLightColors': undefined
    });
    $mdThemingProvider.definePalette('boltAccentPalette', {
      '50': '000',
      '100': '000',
      '200': '000',
      '300': 'f4bd5f',
      '400': 'f4bd5f',
      '500': 'f4bd5f',
      '600': '000',
      '700': '000',
      '800': 'f4bd5f',
      '900': '000',
      'A100': '000',
      'A200': 'f4bd5f',
      'A400': '777',
      'A700': '333',
      'contrastDefaultColor': 'light'
    });
    $mdThemingProvider.definePalette('boltWarnPalette', {
      '50': '666',
      '100': '000',
      '200': '000',
      '300': '000',
      '400': 'f4bd5f',
      '500': 'e56d51',
      '600': 'f00',
      '700': '666',
      '800': '999',
      '900': '000',
      'A100': '000',
      'A200': '000',
      'A400': '999',
      'A700': 'e56d51',
      'contrastDefaultColor': 'light'
    });
    
    $mdThemingProvider.theme('bolt')
    .primaryPalette('boltPrimaryPalette')
    .warnPalette('boltWarnPalette')
    .accentPalette('boltAccentPalette');
    
  }
]).config([
  '$mdIconProvider', 
  function(
    $mdIconProvider
  ){
    $mdIconProvider
    .defaultIconSet('/styles/svg-sprite-icons.svg', 24);
  }
]);
