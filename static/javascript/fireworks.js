//   ===============================================================
// كود الالعاب النارية عند وصول هدية
document.addEventListener('DOMContentLoaded', function() {
    const showGiftCardInput = document.getElementById('show-gift-card');
  
    // تحقق من وجود العناصر في الصفحة
    if (showGiftCardInput) {
        showGiftCardInput.addEventListener('change', function() {
            if (showGiftCardInput.checked) {
                
                var tceW3C   = 0; //#BCON
                var tceIE    = 1; //#BCON
                var tceOther = 2; //#BCON

                var myChangeEvent = (function () {

                    var mtypeOfChangeEventThatBrowserSupports;

                    function initialise()
                    {
                        var sampleHTMLElement = document.body;

                        if (sampleHTMLElement.addEventListener) { // W3C DOM

                        mtypeOfChangeEventThatBrowserSupports = tceW3C;

                        } else if (sampleHTMLElement.attachEvent) { // IE DOM

                        mtypeOfChangeEventThatBrowserSupports = tceIE;
                        }
                        else {

                        mtypeOfChangeEventThatBrowserSupports = tceOther;
                        }    

                    }

                    function add(event, HTMLElement, func)
                    {
                        switch(mtypeOfChangeEventThatBrowserSupports) {

                            case tceW3C:
                                HTMLElement.addEventListener(event, func, false);
                                break;
                            case tceIE:
                                HTMLElement.attachEvent('on' + event, func);
                                break;
                            default:
                                HTMLElement['on' + event] = func;
                                break;
                        }
                    }

                    function remove(event, HTMLElement, func)
                    {
                        switch(mtypeOfChangeEventThatBrowserSupports) {

                            case tceW3C:
                                HTMLElement.removeEventListener(event, func, false);
                                break;
                            case tceIE:
                                HTMLElement.detachEvent('on' + event, func);
                                break;
                            default:
                                HTMLElement['on' + event] = null;
                                break;
                        }
                    }

                    initialise();

                    return {
                        add    : add, 
                        remove : remove
                    };

                })(); 

                function SessIon()
                {
                }
                var session = new SessIon();

                var _Session_prototype = SessIon.prototype;

                /* is there a black on white color scheme ? */ 

                var defaultIsMoreContrast = false; //#BCON

                var ismorecontrast = defaultIsMoreContrast;
                //var ismorecontrast = true;

                /* is there a black background? */ 

                var defaultDarkBackground = false; //#BCON

                var isdarkbackground = defaultDarkBackground;
                var isdarkbackground = true;

                /* is 'dark mode' implemented by using an 'invert' filter or
                are all the colours changed one-by-one? */

                var dmCustom = 0; //#BCON
                //var dmInvert = 1; //#BCON

                //TODO:bernardo
                var gDefaultTypeOfDarkMode = dmCustom;
                //var gDefaultTypeOfDarkMode = dmInvert;

                /* is 'dark mode' implemented by using an 'invert' filter or
                are all the colours changed one-by-one? */

                var dmCustom = 0; //#BCON
                //var dmInvert = 1; //#BCON

                //TODO:bernardo
                var gDefaultTypeOfDarkMode = dmCustom;
                //var gDefaultTypeOfDarkMode = dmInvert;

                var gTypeOfDarkMode = gDefaultTypeOfDarkMode;

                _Session_prototype.setupFireworkDoodle = function(headelement)

                /* The code below, for the fireworks animation, has an 'MIT' license.
                The MIT license is at the top of this source code. 
                Copyright (c) 2024 by Yusuke Nakaya (https://codepen.io/YusukeNakaya/pen/zYvWGwb) */

                {
                    var fireworkDoodle;

                //            if (!gDoesBrowserSupportPaperbirdDoodle) {
                //                //TODO: rm
                //                //alert('firework:!supp');
                //                return;
                //            }

                    this.FireworkDoodle = 

                        fireworkDoodle = (function (tSession) {

                        var mMyChangeevent;
                        var mHeadElement;

                        var mFireworkStylesheet;
                        var mContainer; 
                        var mDoc; 


                        function initialise(myChangeevent, headElement)
                        {
                            mMyChangeevent = myChangeevent;

                            mHeadElement = headElement;

                            mDoc = document;
                        }

                        function start()
                        {
                            var doc = mDoc;

                            function getRandomColorBlue() {
                            return 'rgb(' + (Math.round(Math.random() * 100) + 50) +
                                            ',' + 
                                            (Math.round(Math.random() * 100) + 50) + 
                                            ',' +
                                            (Math.round(Math.random() *  55) + 150) +
                                            ')';
                            }
                            function getRandomColorGreenBlue() {
                            return 'rgb(' + (Math.round(Math.random() * 100) + 50) + 
                                            ',' + 
                                            (Math.round(Math.random() *  55) + 150) +
                                            ',' +
                                            (Math.round(Math.random() *  55) + 150) +
                                            ')';
                            }
                            function getRandomColorRed() {
                            return 'rgb(' + (Math.round(Math.random() *  55) + 150) +
                                            ',' + 
                                            (Math.round(Math.random() * 100) + 50) +
                                            ',' +
                                            (Math.round(Math.random() * 100) + 50) + 
                                            ')';
                            }
                            function getRandomColorRedBlue() {
                            return 'rgb(' + (Math.round(Math.random() *  55) + 150) +
                                            ',' + 
                                            (Math.round(Math.random() * 100) + 50) + 
                                            ',' +
                                            (Math.round(Math.random() *  55) + 150) +
                                            ')';
                            }
                            function getRandomColorRedGreen() {
                            return 'rgb(' + (Math.round(Math.random() *  55) + 150) +
                                            ',' + 
                                            (Math.round(Math.random() *  55) + 150) +
                                            ',' +
                                            (Math.round(Math.random() * 100) + 50) +
                                            ')';
                            }
                            function getRandomColorGreen() {
                            return 'rgb(' + (Math.round(Math.random() * 100) + 50) + 
                                            ',' + 
                                            (Math.round(Math.random() *  55) + 150) +
                                            ',' +
                                            (Math.round(Math.random() * 100) + 50) + 
                                            ')';
                            }

                            function getRandomColorBlueDM () {
                            return 'rgb(' + (Math.round(Math.random() * 100) + 100) +
                                            ',' + 
                                            (Math.round(Math.random() * 100) + 100) +
                                            ',' +
                                            (Math.round(Math.random() *  55) + 200) +
                                            ')';
                            }
                            function getRandomColorGreenBlueDM () {
                            return 'rgb(' + (Math.round(Math.random() * 100) + 100) +
                                            ',' + 
                                            (Math.round(Math.random() *  55) + 200) +
                                            ',' +
                                            (Math.round(Math.random() *  55) + 200) +
                                            ')';
                            }
                            function getRandomColorRedDM () {
                            return 'rgb(' + (Math.round(Math.random() *  55) + 200) +
                                            ',' + 
                                            (Math.round(Math.random() * 100) + 100) +
                                            ',' +
                                            (Math.round(Math.random() * 100) + 100) +
                                            ')';
                            }
                            function getRandomColorRedBlueDM () {
                            return 'rgb(' + (Math.round(Math.random() *  55) + 200) +
                                            ',' + 
                                            (Math.round(Math.random() * 100) + 100) +
                                            ',' +
                                            (Math.round(Math.random() *  55) + 200) +
                                            ')';
                            }
                            function getRandomColorRedGreenDM () {
                            return 'rgb(' + (Math.round(Math.random() *  55) + 200) +
                                            ',' + 
                                            (Math.round(Math.random() *  55) + 200) +
                                            ',' +
                                            (Math.round(Math.random() * 100) + 100) +
                                            ')';
                            }
                            function getRandomColorGreenDM () {
                            return 'rgb(' + (Math.round(Math.random() * 100) + 100) +
                                            ',' + 
                                            (Math.round(Math.random() *  55) + 200) +
                                            ',' +
                                            (Math.round(Math.random() * 100) + 100) +
                                            ')';
                            }

                            function getRandomColorDM() {

                                var randColorValue = Math.random();
                                var randColor;
                                var randColor2;
                            
                                if (randColorValue < 0.166666) {
                                    randColor = getRandomColorRedDM();
                                    randColor2 = getRandomColorRedDM();
                                } else if (randColorValue < 0.33333) {
                                    randColor = getRandomColorBlueDM();
                                    randColor2 = getRandomColorBlueDM();
                                } else if (randColorValue < 0.5) {
                                    randColor = getRandomColorGreenDM();
                                    randColor2 = getRandomColorGreenDM();
                                } else if (randColorValue < .66666) {
                                    randColor = getRandomColorGreenBlueDM();
                                    randColor2 = getRandomColorGreenBlueDM();
                                } else if (randColorValue < .83333) {
                                    randColor = getRandomColorRedBlueDM();
                                    randColor2 = getRandomColorRedBlueDM();
                                } else {
                                    randColor = getRandomColorRedGreenDM();
                                    randColor2 = getRandomColorRedGreenDM();
                                }
                            
                                return [ randColor, randColor2 ];
                            }


                            function getRandomColorNormal() {

                                var randColorValue = Math.random();
                                var randColor;
                                var randColor2;
                            
                                if (randColorValue < 0.166666) {
                                    randColor = getRandomColorRed();
                                    randColor2 = getRandomColorRed();
                                } else if (randColorValue < 0.33333) {
                                    randColor = getRandomColorBlue();
                                    randColor2 = getRandomColorBlue();
                                } else if (randColorValue < 0.5) {
                                    randColor = getRandomColorGreen();
                                    randColor2 = getRandomColorGreen();
                                } else if (randColorValue < .66666) {
                                    randColor = getRandomColorGreenBlue();
                                    randColor2 = getRandomColorGreenBlue();
                                } else if (randColorValue < .83333) {
                                    randColor = getRandomColorRedBlue();
                                    randColor2 = getRandomColorRedBlue();
                                } else {
                                    randColor = getRandomColorRedGreen();
                                    randColor2 = getRandomColorRedGreen();
                                }
                            
                                return [ randColor, randColor2 ];
                            }

                            function getRandomColor() {

                                var colors;

                                if (isWhiteOnBlack) {
                                    colors = [ 'white', 'white' ];
                                } else if (isBlackOnWhite ) {
                                    colors = [ 'black', 'black' ];
                                } else if (isDarkMode) {
                                    colors = getRandomColorDM();
                                } else {
                                    colors = getRandomColorNormal();
                                }

                                return colors;
                            }

                            var isDarkMode; 
                            var isWhiteOnBlack;
                            var isBlackOnWhite;

                            if (ismorecontrast) {
                                if (isdarkbackground) {
                                    isWhiteOnBlack = true;
                                } else {
                                    isBlackOnWhite = true;
                                }
                            } else {
                                isDarkMode =
                                    (isdarkbackground && 
                                        gTypeOfDarkMode === dmCustom); 
                            }

                            var countFireworks = 3 + Math.round(Math.random() * 4);
                            var countLinesPerFirework;
                            var linesPerFirework = [];
                            
                            var s = '';
                            var fx;
                            var fy;
                            var fz;
                            var fc;
                            var lc;
                            var lRotY;
                            var sparkDeg;
                            var sparkRotYDeg;
                            var sparkKeyFrame0TranslateY;
                            var sparkKeyFrame100TranslateX;
                            var fireDuration; 
                            var fireDelay;
                            var fireWidth;
                            var fireHeight;
                            var fireLeft;
                            var sparkAnimDuration;
                            var sparkAnimDelay = 0;
                            var fireColors;
                            var fireForeColor; 
                            var fireBackColor;
                            var fireworkDuration;
                            var fireRotateX;
                            var fireRotateY;
                            var fireRotateZ;
                            var fireTransform; 
                            var maxFireworkDuration = 0;
                            var fireworkIndexOfMaxDuration; 
                            var upFadeInOpacityPercent; 
                            var upFadeOutOpacityPercent;
                            var outFadeInOpacityPercent;
                            var outFadeOutOpacityPercent;
                            var fcs;
                            
                            var perspective = 400 + Math.round(Math.random() * 400);
                            var perspectiveWithPx = perspective + 'px';

                            s +=
                            ' .frwdStage { ' +
                            '   perspective: ' + perspectiveWithPx + '; ' +
                            ' } ';

                            for (fc = 1; fc <= countFireworks; fc++) {
                            
                                fx = -15 + Math.random() * 30;
                                fy = -Math.random() * 20;
                                fz = -15 + Math.random() * 30;
                            
                                s +=
                                    ' .frwdFireworks:nth-child(' + fc + ') { ' +
                                    '     transform: translate3d(' + fx + 'vw, ' + fy +
                                    'vh, ' + fz + 'vmin); ' +
                                    ' } ';
                            
                                if (fc > 1) {
                            
                                    //nopainnogain
                                    sparkAnimDelay = -Math.random();
                                
                                    s +=
                                        ' .frwdFireworks:nth-child(' + fc + 
                                        ') .frwdLine .frwdSpark { ' +
                                        '          animation-delay: ' + 
                                        sparkAnimDelay + 's; ' +
                                        ' } '; 
                                }
                            
                                fireColors = getRandomColor();
                                fireForeColor = fireColors[0];
                                fireBackColor = fireColors[1];; 

                                s +=
                                    ' .frwdFireworks:nth-child(' + fc + 
                                    ') .frwdLine .frwdSpark .frwdFire { ' +
                                    '    background: ' + fireForeColor + '; ' +
                                    ' } ' +
                                    ' .frwdFireworks:nth-child(' + fc + 
                                    ') .frwdLine .frwdSpark .frwdFire::before { ' +
                                    '    background: ' + fireBackColor + '; ' +
                                    ' } ';
                            
                                sparkAnimDuration = 3.5 + Math.random() * 3;
                            
                                fireworkDuration = sparkAnimDuration + sparkAnimDelay;
                            
                                if (fireworkDuration > maxFireworkDuration) {
                                    maxFireworkDuration = fireworkDuration;
                                    fireworkIndexOfMaxDuration = fc;
                                }
                            
                                fcs = '.frwdFireworks:nth-child(' + fc + ') ';
                            
                                countLinesPerFirework = 50 + 
                                                        Math.round(Math.random() * 50);
                                //TODO:rm
                                //countLinesPerFirework = 1;
                                linesPerFirework[fc] = countLinesPerFirework;
                            
                                for (lc = 1; lc <= countLinesPerFirework; lc++) {
                                
                                    lRotY = Math.random() * 360;
                                
                                    s +=
                                        fcs + ' .frwdLine:nth-child(' + lc + ') { ' +
                                        ' transform: rotate3d(0,1,0,' + lRotY + 'deg);'+
                                        ' } ';
                                
                                    s +=
                                        fcs + ' .frwdLine:nth-child(' + lc + 
                                            ') .frwdSpark { ' +
                                            '     animation: frwdSpark-' + fc + '-' 
                                            + lc + ' ' + sparkAnimDuration + 
                                            's cubic-bezier(0.39, 0.575, 0.565, 1) ' +
                                            'forwards, frwdOpacity-' + fc + '-' + lc +
                                            ' ' + sparkAnimDuration + 
                                            's ease-out forwards; ' +
                                        ' } ';
                                
                                    sparkDeg = (Math.random() * 360) + 'deg';
                                    sparkRotYDeg = (Math.random() * 360) + 'deg';
                                    sparkKeyFrame0TranslateY = 
                                        Math.round(Math.random() * 150 + 500) + 'px';
                                    sparkKeyFrame100TranslateX = 
                                        Math.round(Math.random() * 200 + 100) + 'px';
                                        
                                    s +=
                                        ' @keyframes frwdSpark-' + fc + '-' + lc + 
                                        ' { ' +
                                        '  0% { ' +
                                        '     transform: translate3d(0,' + 
                                        sparkKeyFrame0TranslateY + ',0); ' +
                                        '  } ' +
                                
                                        '  50% { ' +
                                        '    transform: translate3d(0,0,0); ' +
                                        '  } ' +
                                
                                        '  100% { ' +
                                        '    transform: rotate3d(0,0,1,' + sparkDeg + 
                                        ') rotate3d(0,1,0,' + sparkRotYDeg + 
                                        ') translate3d(' + sparkKeyFrame100TranslateX +
                                        ',0,0); ' +
                                        '  } ' +
                                        ' } ';
                            
                                    upFadeInOpacityPercent = 10 + Math.random() * 20;
                                    upFadeOutOpacityPercent = 40 + Math.random() * 5;
                                    outFadeInOpacityPercent = 55 + Math.random() * 10;
                                    outFadeOutOpacityPercent = 85 + Math.random() * 10;
                            
                                    s +=
                                        ' @keyframes frwdOpacity-' + fc + '-' + lc + 
                                        ' { ' +
                                        '   0% { ' +
                                        '     opacity: 0; ' +
                                        '   } ' +
                                        '    ' +
                                        '   ' + upFadeInOpacityPercent + '% { ' +
                                        '     opacity: 1; ' +
                                        '   } ' +
                                        '    ' +
                                        '   ' + upFadeOutOpacityPercent + '% { ' +
                                        '     opacity: 0; ' +
                                        '   } ' +
                                        '    ' +
                                        '   50% { ' +
                                        '     opacity: 0; ' +
                                        '   } ' +
                                        '    ' +
                                        '   ' + outFadeInOpacityPercent + '% { ' +
                                        '     opacity: 1; ' +
                                        '   } ' +
                                        '    ' +
                                        '   ' + outFadeOutOpacityPercent + '% { ' +
                                        '     opacity: 1; ' +
                                        '   } ' +
                                        '    ' +
                                        '   100% { ' +
                                        '     opacity: 0; ' +
                                        '   } ' +
                                        ' } ';
                            
                                    fireDuration = Math.random() * 1000 + 1000;
                                    fireDelay = Math.random() * fireDuration;
                            
                                    fireWidth = 0.25 + Math.random() * 0.15;
                                    fireHeight = 0.25 + Math.random() * 0.15;
                                    fireLeft = fireWidth / 2;
                                
                                    s +=
                                        fcs + ' .frwdLine:nth-child(' + lc + 
                                        ') .frwdFire { ' +
                                        '     animation: frwdFire-' + fc + '-' + lc + 
                                        ' ' + fireDuration + 'ms -' + fireDelay + 
                                        'ms linear infinite; ' +
                                        ' left: -' + fireLeft + 'em; ' +
                                        ' width: ' + fireWidth + 'em; ' +
                                        ' height: ' + fireHeight + 'em; ' +
                                        ' } '; 
                            
                                    fireRotateX = Math.ceil(Math.random() * 3) * 360;
                                    fireRotateY = Math.ceil(Math.random() * 3) * 360;
                                    fireRotateZ = Math.ceil(Math.random() * 3) * 360;
                            
                                    fireTransform = 
                                        'rotate3d(1,0,0,' + fireRotateX + 
                                        'deg) rotate3d(0,1,0,' + fireRotateY + 
                                        'deg) rotate3d(0,0,1,' + fireRotateZ + 'deg)';
                            
                                    s +=
                                        ' @keyframes frwdFire-' + fc + '-' + lc + 
                                            ' { ' +
                                            '  0% { ' +
                                            '    transform: rotate3d(1,0,0,0deg) ' + 
                                            'rotate3d(0,1,0,0deg) ' + 
                                            'rotate3d(0,0,1,0deg); ' +
                                            '  } ' +
                                            '   ' +
                                            '  100% { ' +
                                            '    transform: ' + fireTransform + '; ' +
                                            '  } ' +
                                        ' } ';
                                
                                } // each line
                            
                            } // each firework 

                            var fireworkStylesheet = doc.createElement('style');
                            mFireworkStylesheet = fireworkStylesheet;
                            fireworkStylesheet.innerHTML = s;

                            mHeadElement.appendChild(fireworkStylesheet);

                            var fwe;
                            var le;
                            var se;
                            var fre;
                            var container = doc.createElement('div');
                            container.className = 'frwdStage';
                            mContainer = container; 
                            
                            for (fc = 1; fc <= countFireworks; fc++) {
                            
                                fwe = doc.createElement('div');
                                fwe.className = 'frwdFireworks';
                            
                                countLinesPerFirework = linesPerFirework[fc];
                            
                                for (lc = 1; lc <= countLinesPerFirework; lc++) {
                            
                                    fre = doc.createElement('div');
                                    fre.className = 'frwdFire';
                                    se = doc.createElement('div');
                                    se.className = 'frwdSpark';
                                    le = doc.createElement('div');
                                    le.className = 'frwdLine';
                            
                                    if (lc === 1 && fc === fireworkIndexOfMaxDuration) {
                                        mMyChangeevent.add('animationend', se, end);
                                    } 
                            
                                    se.appendChild(fre);
                                    le.appendChild(se);
                                    fwe.appendChild(le);
                                }
                            
                                container.appendChild(fwe);
                            
                            }
                            
                            doc.body.appendChild(container);

                        } // end function start()

                        function clear()
                        {
                            if (!mContainer) {
                                session.doodle = null;
                                //TODO: rm
                                //alert('firew:noContainer');
                                return;
                            }

                            mDoc.body.removeChild(mContainer);

                            mHeadElement.removeChild(mFireworkStylesheet);

                            mContainer = null;
                            mFireworkStylesheet = null;

                            tSession.doodle = null;
                        }

                        function end(e)
                        {
                            //TODO: rm
                            //alert('end');

                            var startOfAnimName = e.animationName.substr(0,11);

                            if (startOfAnimName === 'frwdOpacity') {
                                //TODO: rm
                                //alert('end:clear');
                                clear();
                            }
                        }

                        function stop()
                        {
                            clear();
                        }

                        function hide()
                        {
                            mContainer.style.top = '-9999px';
                        }

                        function showAfterHide()
                        {
                            mContainer.style.top = '';
                        }

                        return {
                            initialise    : initialise,
                            start         : start,
                            stop          : stop, 
                            hide          : hide,
                            showAfterHide : showAfterHide
                        };

                    })(this); 

                    fireworkDoodle.initialise(
                        myChangeEvent, 
                        headelement
                    );

                //            var doodles = this.doodles;
                //            doodles[doodles.length] = fireworkDoodle; 

                }; // end of Session setupFireworkDoodle function

                var gHeadElement = document.getElementsByTagName('head')[0];

                session.setupFireworkDoodle(gHeadElement);

                session.FireworkDoodle.start();
                            } 
        });
    }
      
  });
//   ===============================================================
