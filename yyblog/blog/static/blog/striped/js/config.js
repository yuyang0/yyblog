/*
	Striped 2.0 by HTML5 Up!
	html5up.net | @n33co
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
*/

// function get_css_prefix () {
// 	var pathArray = window.location.pathname.split( '/' );
// 	var newPathname = "";
// for ( i = 0; i < pathArray.length; i++ ) {
//   newPathname += "/";
//   if (pathArray[i] == "js") 
//   	{
//   		newPathname += "css/style";
//   		return newPathname;
//   	};
//   newPathname += pathArray[i];
// }
// }

window._5grid_config = {
	prefix: '/static/blog/striped/css/style',
	// prefix: get_css_prefix()
	useResets: true,
	useOrientation: true,
	grid: {
		containers: 1200
	},
	breakpoints: {
		'mobile': {
			range: '-640',
			lockViewport: true,
			grid: {
				containers: 'fluid',
				collapse: true
			}
		},
		'desktop': {
			range: '641-',
			grid: {
				containers: 1200
			}
		},
		'wide': {
			range: '1201-'
		},
		'narrow': {
			range: '641-1200',
			grid: {
				containers: 960
			}
		},
		'narrower': {
			range: '641-1000'
		}
	}
};

window._5grid_ui_config = {
	panels: {
		sidePanel: {
			breakpoints: 'mobile',
			position: 'left',
			style: 'reveal',
			size: '250px',
			html: '<div data-action="moveElement" data-target="sidebar"></div>'			
		},
		sidePanelNarrower: {
			breakpoints: 'narrower',
			position: 'left',
			style: 'reveal',
			size: '300px',
			html: '<div data-action="moveElement" data-target="sidebar"></div>'			
		}
	},
	bars: {
		titleBar: {
			breakpoints: 'mobile',
			position: 'top',
			size: 44,
			style: 'floating',
			html: '<div class="toggle " data-action="panelToggle" data-target="sidePanel"></div>' +
				  '<div class="title" data-action="copyHTML" data-target="logo"></div>'
		},
		titleBarNarrower: {
			breakpoints: 'narrower',
			position: 'top',
			size: 60,
			style: 'floating',
			html: '<div class="toggle " data-action="panelToggle" data-target="sidePanelNarrower"></div>' +
				  '<div class="title" data-action="copyHTML" data-target="logo"></div>'
		}
	}
};