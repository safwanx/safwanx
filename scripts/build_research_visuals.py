"""Build profile visuals. Usage: python scripts/build_research_visuals.py PATH_TO_CROWDSENSE

Requires Pillow, numpy and opencv-python. Uses existing video outputs, not fresh inference.
"""
from pathlib import Path
import math
import sys
import cv2
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)
BG, INK, MUTED = '#152b3c', '#e7f0e5', '#abc6c9'

def svg(title, body, extra=''):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="240" viewBox="0 0 1000 240" role="img" aria-labelledby="title">
<title id="title">{title}</title>
<style>text{{font-family:'Segoe UI',sans-serif;fill:{INK}}}.small{{font-size:14px;fill:{MUTED}}}.label{{font-size:17px;font-weight:600}}.flow{{stroke-dasharray:5 11;animation:travel 3s linear infinite}}@keyframes travel{{to{{stroke-dashoffset:-64}}}}@media(prefers-reduced-motion:reduce){{*{{animation:none!important}}}}{extra}</style>
<rect width="1000" height="240" rx="16" fill="{BG}"/>
{body}</svg>'''

# Four region encoders, learned fusion, temporal modeling; conceptual, not a sign sample.
body = '<text x="28" y="30" class="small">TWASEL / Four views of one movement</text>'
body += '<g fill="none" stroke="#6b8794" stroke-width="3" stroke-linecap="round"><circle cx="105" cy="91" r="21"/><path d="M105 114v55m-32-45h64m-64 0-15 36 30-10m49-26 20 27-30 12m-22 6-24 35m24-35 25 35"/></g>'
body += '<g fill="#b8b7e9"><circle cx="97" cy="87" r="3"/><circle cx="112" cy="87" r="3"/><circle cx="105" cy="100" r="3"/></g>'
body += '<g fill="#91d2c1"><circle cx="73" cy="124" r="4"/><circle cx="137" cy="124" r="4"/><circle cx="105" cy="169" r="4"/></g>'
body += '<g fill="#e3c77c"><circle cx="88" cy="150" r="6"/><circle cx="127" cy="163" r="6"/></g>'
body += '<text x="40" y="225" class="small">Pose keypoints</text>'
for y, label, color in [(65,'Body','#91d2c1'),(107,'Left hand','#e3c77c'),(149,'Right hand','#dcaa91'),(191,'Face','#b8b7e9')]:
    body += f'<path d="M177 127Q212 {y} 244 {y}" fill="none" stroke="{color}" opacity=".35"/>'
    body += f'<circle cx="249" cy="{y}" r="4" fill="{color}"/><text x="265" y="{y+6}" class="label">{label}</text>'
    body += f'<path d="M374 {y}C452 {y} 439 126 509 126" fill="none" stroke="{color}" stroke-width="2" class="flow"/>'
body += '<circle cx="535" cy="126" r="24" fill="#294b59" stroke="#91d2c1"/><path d="m524 126 8 8 15-16" fill="none" stroke="#91d2c1" stroke-width="2"/>'
body += '<text x="483" y="184" class="label">Learned fusion</text><path d="M560 126h68m122 0h69" stroke="#91d2c1" stroke-width="2" class="flow"/>'
for x in range(632,746,17):
    h=22+21*math.sin(x*.035)**2
    body += f'<rect x="{x}" y="{126-h}" width="9" height="{2*h}" rx="4" fill="#8bb8c9"/>'
body += '<text x="630" y="184" class="label">Conformer</text>'
body += '<g fill="#b8b7e9"><rect x="827" y="102" width="36" height="15" rx="4"/><rect x="870" y="102" width="57" height="15" rx="4"/><rect x="827" y="128" width="67" height="15" rx="4"/><rect x="901" y="128" width="24" height="15" rx="4"/></g>'
body += '<text x="820" y="184" class="label">Gloss sequence</text><text x="780" y="224" class="small">Architecture sketch, not inference</text>'
(OUT/'twasel-streams.svg').write_text(svg('TWASEL architecture sketch: body, left hand, right hand and face streams join through learned fusion, then temporal modeling and gloss decoding.',body),encoding='utf-8')

# Do not invent measurements: this is an explanatory drawing, explicitly labelled.
body = '<text x="28" y="30" class="small">CROWD RELIABILITY / A good ranking is only half the story</text>'
for i in range(10):
    x=32+(i%5)*47; y=68+(i//5)*47
    body += f'<rect x="{x}" y="{y}" width="36" height="32" rx="5" fill="#294b59"/>'
    for j in range(3+i%3):
        px=x+7+(j%3)*10; py=y+9+(j//3)*13
        body += f'<circle cx="{px}" cy="{py}" r="2.3" fill="#91d2c1"/>'
body += '<text x="32" y="186" class="label">Different crowd images</text>'
body += '<path d="M279 107h47" stroke="#91d2c1" stroke-width="2" class="flow"/>'
for i in range(10):
    x=345+i*24; h=18+i*6
    body += f'<rect x="{x}" y="{145-h}" width="15" height="{h}" rx="3" fill="'+('#e3c77c' if i>=8 else '#91d2c1')+'"/>'
body += '<text x="345" y="185" class="label">Rank predicted error risk</text><text x="345" y="209" class="small">Lower</text><text x="536" y="209" class="small">Higher</text>'
body += '<path d="M604 107h46" stroke="#91d2c1" stroke-width="2" class="flow"/>'
body += '<path d="M680 147V66m0 81h100" stroke="#698894" fill="none"/><path d="m687 139 83-65" stroke="#698894" stroke-dasharray="4 5"/>'
body += '<path d="M687 138Q729 136 771 86" fill="none" stroke="#e3c77c" stroke-width="2.5"/>'
body += '<text x="801" y="89" class="label">New dataset.</text><text x="801" y="114" class="label">Same confidence?</text><text x="681" y="185" class="small">Ranking can hold up while</text><text x="681" y="207" class="small">calibration breaks.</text>'
body += '<text x="28" y="225" class="small">Conceptual illustration; bars and curves are not measured results.</text>'
(OUT/'crowd-reliability.svg').write_text(svg('Conceptual illustration of crowd-image risk ranking and calibration under dataset shift. Not measured data.',body),encoding='utf-8')

if len(sys.argv)>1:
    media=Path(sys.argv[1])/'media'
    names=['crowd_vid1.mp4','density.mp4','overlay.mp4']
    caps=[cv2.VideoCapture(str(media/n)) for n in names]
    assert all(c.isOpened() for c in caps)
    assert all(int(c.get(cv2.CAP_PROP_FRAME_COUNT))==341 for c in caps)
    fonts=Path('C:/Windows/Fonts')
    font=lambda size: ImageFont.truetype(str(fonts/'segoeui.ttf'),size)
    heading, label, small=font(25),font(18),font(15)
    frames=[]
    # Every panel uses the identical source frame index. Six seconds at 8 fps.
    for i in range(48):
        frame_index=25+round(i*25/8)
        canvas=Image.new('RGB',(960,330),BG); draw=ImageDraw.Draw(canvas)
        draw.text((24,15),'CrowdSense',font=heading,fill=INK)
        draw.text((192,24),'One scene, three views',font=small,fill=MUTED)
        for k,(cap,name) in enumerate(zip(caps,['Input video','Predicted density','Density overlay'])):
            cap.set(cv2.CAP_PROP_POS_FRAMES,frame_index)
            ok, frame=cap.read(); assert ok
            im=Image.fromarray(cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)).resize((296,167),Image.Resampling.LANCZOS)
            x=24+k*308
            draw.text((x,66),name,font=label,fill=INK)
            canvas.paste(im,(x,98))
        draw.line((24,282,936,282),fill='#35515e',width=2)
        draw.line((24,282,24+int(912*(i+1)/48),282),fill='#91d2c1',width=3)
        draw.text((24,300),'Existing CrowdSense demo outputs · synchronized frames',font=small,fill=MUTED)
        draw.text((788,300),f'{frame_index/25:04.1f}s / video',font=small,fill=MUTED)
        frames.append(canvas)
    for cap in caps: cap.release()
    frames[16].save(OUT/'crowdsense-demo.png',optimize=True)
    palette=frames[16].quantize(colors=128)
    indexed=[f.quantize(palette=palette,dither=Image.Dither.NONE) for f in frames]
    indexed[0].save(OUT/'crowdsense-demo.gif',save_all=True,append_images=indexed[1:],duration=125,loop=0,optimize=True)
    print('GIF bytes:',(OUT/'crowdsense-demo.gif').stat().st_size)
print('Visuals written to',OUT)
