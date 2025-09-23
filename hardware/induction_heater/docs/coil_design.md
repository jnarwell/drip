# Induction Work Coil Design and Winding Procedure

## Design Specifications

### Calculated Parameters
- **Coil Diameter**: 80mm (crucible 60mm + 10mm clearance each side)
- **Number of Turns**: 8
- **Turn Spacing (Pitch)**: 10mm
- **Total Height**: 80mm
- **Copper Tube**: 6mm OD × 4mm ID
- **Inductance**: ~15μH
- **Resonant Frequency**: ~71kHz (with 0.33μF capacitor bank)
- **Copper Length Required**: 2.0m (plus 300mm for leads)

### Materials List
- 2.5m of 6mm OD copper refrigeration tubing (soft annealed)
- Fine sand for tube filling
- 2× rubber caps for tube ends
- 80mm diameter PVC pipe (winding form)
- 2× 6mm compression fittings with G1/4" thread
- 2× 100A copper lugs (6mm hole)
- Silver solder and flux
- NO-OX-ID conductive grease
- Heat shrink tubing

## Winding Procedure

### Step 1: Prepare the Copper Tube
1. **Clean the tube**
   - Use fine sandpaper (220 grit) to remove oxidation
   - Wipe with isopropyl alcohol
   - Ensure no dents or kinks

2. **Fill with sand**
   - Use dry, fine sand (playground sand works well)
   - Fill tube completely, tapping to settle
   - Cap both ends tightly with rubber caps
   - This prevents tube collapse during bending

### Step 2: Create the Winding Form
1. **Mark the form**
   - Use 80mm OD PVC pipe, ~150mm long
   - Mark spiral at 10mm pitch
   - Start mark 20mm from bottom

2. **Create guide groove** (optional)
   - Use rotary tool to cut 3mm deep groove
   - Follow spiral marking
   - Helps maintain consistent spacing

### Step 3: Wind the Coil
1. **Start the first turn**
   - Leave 150mm straight section for connection
   - Begin winding at bottom mark
   - Keep tube against form firmly

2. **Continue winding**
   - Follow the 10mm pitch carefully
   - Maintain even pressure
   - Complete 8 full turns
   - Leave 150mm straight at top

3. **Check dimensions**
   - Verify 80mm outer diameter
   - Confirm 80mm total height
   - Ensure turns are parallel

### Step 4: Remove Sand and Install Fittings
1. **Remove sand**
   - Remove end caps carefully
   - Flush with water thoroughly
   - Use compressed air to ensure complete removal
   - Any remaining sand will damage pump!

2. **Solder water fittings**
   - Clean tube ends to bright copper
   - Apply flux liberally
   - Heat evenly and apply silver solder
   - Use 6mm compression to G1/4" adapters

3. **Pressure test**
   - Cap one end, apply 3 bar (45 PSI) air pressure
   - Submerge in water to check for leaks
   - Hold pressure for 10 minutes

### Step 5: Install Electrical Connections
1. **Prepare connection points**
   - File/sand flat spots on straight sections
   - Clean to bright copper
   - These carry up to 100A - must be perfect

2. **Attach copper lugs**
   - Use 100A rated lugs with 6mm holes
   - Apply NO-OX-ID compound before attachment
   - Use stainless steel bolts with lock washers
   - Torque to 15 Nm (11 ft-lbs)

3. **Insulate connections**
   - Use large heat shrink over lugs
   - Ensure no exposed copper except coil
   - Label positive and negative

## Critical Dimensions Diagram

```
     Side View                    Top View
     
    ←── 150mm ──→                    80mm
    ____________                  ╱─────────╲
   |            |═══╗           ╱             ╲
   |            |   ║          │               │
   |    80mm    |   ║ 8 turns │    Crucible   │
   |            |   ║  @10mm   │     60mm      │
   |            |   ║          │               │
   |____________|═══╝           ╲             ╱
    ←── 150mm ──→                 ╲─────────╱
                                  ←─ 10mm →←→ 10mm
```

## Installation in System

### Mounting
1. **Position coil**
   - Center over crucible location
   - Bottom of coil 20mm above crucible bottom
   - Use ceramic or PTFE standoffs

2. **Connect cooling**
   - Use 6mm ID silicone tubing
   - Route to avoid heat sources
   - Secure with clamps (no zip ties near coil)

3. **Connect power**
   - Use 8 AWG welding cable minimum
   - Keep leads as short as possible
   - Twist leads together to minimize inductance

### Commissioning Tests
1. **Continuity**: <0.1Ω between terminals
2. **Isolation**: >1MΩ to ground
3. **Water flow**: >2 L/min with no leaks
4. **Resonance**: Verify 30-80kHz with module

## Operating Guidelines

### Do's
- Always run cooling BEFORE applying power
- Check water flow regularly
- Monitor coil temperature (<60°C)
- Keep coil clean and free of metal debris
- Retighten connections monthly

### Don'ts
- Never run without water flow
- Don't exceed 3kW input power
- Avoid ferrous objects near coil
- Don't modify turn count or spacing
- Never bypass temperature limits

## Troubleshooting

| Problem | Possible Cause | Solution |
|---------|---------------|----------|
| Poor heating | Low coupling | Move coil closer (5mm min) |
| Coil overheating | Low water flow | Check pump and filters |
| Arcing | Loose connection | Retighten and clean |
| No resonance | Wrong inductance | Verify 8 turns exactly |
| Uneven heating | Coil not centered | Adjust position |

## Maintenance Schedule

- **Daily**: Check water flow and temperature
- **Weekly**: Inspect for arcing or discoloration  
- **Monthly**: Tighten electrical connections
- **Quarterly**: Clean coil with brass brush
- **Annually**: Replace water and flush system