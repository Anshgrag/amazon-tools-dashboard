from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

file_path = "/mnt/data/Photonics_Module4_Core_Concepts.pdf"

doc = SimpleDocTemplate(file_path, pagesize=A4)
styles = getSampleStyleSheet()
story = []

content = """
<b>MODULE 4: LASERS & OPTICAL FIBERS – CORE CONCEPTS (Simplified)</b><br/><br/>

<b>PART 1: LASERS</b><br/><br/>

<b>What is a LASER?</b><br/>
LASER stands for Light Amplification by Stimulated Emission of Radiation. It is a device that produces highly focused, intense, and coherent light using stimulated emission of photons.<br/><br/>

<b>Key Properties of Laser Light</b><br/>
• Monochromatic (single wavelength)<br/>
• Coherent (waves are in phase)<br/>
• Highly directional (travels straight)<br/>
• Very low divergence (spreads very little)<br/><br/>

<b>Interaction of Radiation with Matter</b><br/>
1. Absorption – atom absorbs photon and gets excited<br/>
2. Spontaneous emission – excited atom emits photon randomly<br/>
3. Stimulated emission – excited atom emits photon identical to incident photon (basis of laser)<br/><br/>

<b>Stimulated Emission (Core Principle)</b><br/>
An incoming photon forces an excited atom to emit another photon with the same energy, phase, and direction. This produces coherent light amplification.<br/><br/>

<b>Conditions for Laser Action</b><br/>
• Population inversion (more atoms in excited state than ground state)<br/>
• Metastable state (longer-lived excited state)<br/>
• Optical resonant cavity (mirrors to amplify light)<br/><br/>

<b>Population Inversion</b><br/>
Normally atoms stay in lower energy states. Laser action requires artificially maintaining more atoms in higher energy states using pumping.<br/><br/>

<b>Pumping Methods</b><br/>
• Optical pumping (flash lamps)<br/>
• Electrical pumping (current or discharge)<br/>
• Semiconductor pumping (electron-hole recombination)<br/><br/>

<b>Metastable States</b><br/>
• Three-level system – pulsed lasers (Ruby laser)<br/>
• Four-level system – continuous lasers (He-Ne laser)<br/><br/>

<b>Einstein Coefficients</b><br/>
• A21 – spontaneous emission probability<br/>
• B12 – absorption probability<br/>
• B21 – stimulated emission probability<br/>
Used to explain equilibrium energy density and laser feasibility.<br/><br/>

<b>Semiconductor Laser</b><br/>
• Based on p-n junction<br/>
• Population inversion achieved via heavy forward bias<br/>
• Uses electron-hole recombination<br/>
• Compact, efficient, continuous output<br/>
• Used in optical communication, CD/DVD drives<br/><br/>

<b>Single Photon Sources & Detectors</b><br/>
• Attenuators reduce laser intensity to approximate single photons<br/>
• SPAD detects single photons using avalanche effect (room temperature)<br/>
• SNSPD detects photons with very high efficiency but needs cryogenic cooling<br/><br/>

<b>PART 2: OPTICAL FIBERS</b><br/><br/>

<b>What is an Optical Fiber?</b><br/>
A thin glass fiber that transmits data using light via total internal reflection. Supports very high bandwidth communication.<br/><br/>

<b>Construction</b><br/>
• Core – carries light (high refractive index)<br/>
• Cladding – reflects light (lower refractive index)<br/>
• Jacket – protects fiber<br/><br/>

<b>Total Internal Reflection</b><br/>
Occurs when light strikes boundary at angle greater than critical angle and gets fully reflected inside the core.<br/><br/>

<b>Acceptance Angle & Numerical Aperture (NA)</b><br/>
• Acceptance angle: maximum angle light can enter fiber<br/>
• Numerical Aperture: light gathering ability of fiber<br/>
NA = √(n1² − n2²)<br/><br/>

<b>V-Number (Normalized Frequency)</b><br/>
• Determines number of modes supported<br/>
• If V < 2.405 → single-mode fiber<br/>
• If V > 2.405 → multimode fiber<br/><br/>

<b>Number of Modes</b><br/>
For multimode fiber: M ≈ V² / 2<br/><br/>

<b>Losses in Optical Fiber (Attenuation)</b><br/>
• Absorption loss (impurities)<br/>
• Scattering loss (Rayleigh scattering)<br/>
• Bending loss (macro & micro bends)<br/><br/>

<b>Types of Optical Fibers</b><br/>
1. Single-mode step-index – long distance, high speed<br/>
2. Multimode step-index – short distance, low bandwidth<br/>
3. Multimode graded-index – medium distance, reduced dispersion<br/><br/>

<b>Fiber Optic Communication System</b><br/>
• Transmitter converts electrical to optical signal<br/>
• Optical fiber transmits signal<br/>
• Repeaters amplify signal<br/>
• Receiver converts optical to electrical signal<br/><br/>

<b>Advantages of Optical Fiber</b><br/>
• High bandwidth<br/>
• Low loss<br/>
• Immune to electromagnetic interference<br/>
• Secure and lightweight<br/><br/>

<b>FINAL TAKEAWAY</b><br/>
Lasers generate coherent light using stimulated emission and population inversion, while optical fibers efficiently guide this light over long distances using total internal reflection.
"""

for line in content.split("\n\n"):
    story.append(Paragraph(line, styles["Normal"]))
    story.append(Spacer(1, 10))

doc.build(story)

file_path
