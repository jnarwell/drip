package ThermalDynamics {
    import ScalarValues::*;
    import ISQ::*;
    import SI::*;
    
    // Droplet Cooling Model
    calc def DropletCoolingModel {
        doc /* 
         * Thermal behavior model for droplet cooling in flight
         * Combines Newton's law of cooling with radiation effects
         */
        
        // Input parameters
        in dropletTemp : TemperatureValue;           // Current droplet temperature
        in ambientTemp : TemperatureValue = 300[K];  // Chamber ambient
        in dropletRadius : LengthValue;              // Droplet size
        in material : MaterialProperties;            // Material properties
        in gasVelocity : VelocityValue;             // Relative gas velocity
        
        // Calculated values
        attribute surfaceArea = 4 * π * dropletRadius^2;
        attribute volume = 4/3 * π * dropletRadius^3;
        attribute mass = material.density * volume;
        
        // Heat transfer coefficients
        attribute reynoldsNumber = gasVelocity * 2 * dropletRadius / gasKinematicViscosity;
        attribute nusseltNumber = 2 + 0.6 * reynoldsNumber^0.5 * prandtlNumber^0.33;
        attribute convectionCoeff = nusseltNumber * gasThermaConductivity / (2 * dropletRadius);
        
        // Newton's law of cooling (convection)
        attribute convectiveHeat = convectionCoeff * surfaceArea * (dropletTemp - ambientTemp);
        
        // Stefan-Boltzmann radiation
        attribute emissivity : Real = 0.3;  // Liquid metal emissivity
        attribute radiativeHeat = emissivity * stefanBoltzmann * surfaceArea * 
                                 (dropletTemp^4 - ambientTemp^4);
        
        // Total heat loss rate
        attribute totalHeatLoss = convectiveHeat + radiativeHeat;
        
        // Temperature change rate
        return coolingRate : TemperatureRateValue = -totalHeatLoss / (mass * material.specificHeat);
        
        // Constraint for SR010 requirement
        constraint highCoolingRate {
            doc /* Cooling rate must exceed 1000°C/s per SR010 */
            coolingRate > 1000[K/s]
        }
    }
    
    // Material-specific Thermal Properties
    part def ThermalMaterialProperties {
        attribute liquidusTempperature : TemperatureValue;
        attribute solidusTemperature : TemperatureValue;
        attribute latentHeatFusion : SpecificEnergyValue;
        attribute thermalExpansion : LinearExpansionCoeffValue;
        
        // Temperature-dependent properties
        calc thermalConductivity(T: TemperatureValue) : ThermalConductivityValue;
        calc specificHeat(T: TemperatureValue) : SpecificHeatCapacityValue;
        calc density(T: TemperatureValue) : MassPerVolumeValue;
    }
    
    part aluminumThermal :> ThermalMaterialProperties {
        :>> liquidusTemperature = 660[°C];
        :>> solidusTemperature = 660[°C];  // Pure Al
        :>> latentHeatFusion = 398[kJ/kg];
        :>> thermalExpansion = 25e-6[1/K];
        
        :>> calc thermalConductivity(T) {
            // Liquid aluminum thermal conductivity
            return 90[W/(m*K)] when T > liquidusTemperature
            else 237[W/(m*K)]  // Solid value
        }
        
        :>> calc specificHeat(T) {
            // Temperature-dependent specific heat
            return 1.18[kJ/(kg*K)] when T > liquidusTemperature
            else 0.90[kJ/(kg*K)]
        }
        
        :>> calc density(T) {
            // Liquid aluminum density with thermal expansion
            attribute T0 = 700[°C];
            attribute rho0 = 2375[kg/m^3];
            return rho0 * (1 - thermalExpansion * (T - T0))
        }
    }
    
    part steelThermal :> ThermalMaterialProperties {
        :>> liquidusTemperature = 1510[°C];
        :>> solidusTemperature = 1450[°C];  // Carbon steel range
        :>> latentHeatFusion = 270[kJ/kg];
        :>> thermalExpansion = 15e-6[1/K];
        
        :>> calc thermalConductivity(T) {
            return 25[W/(m*K)] when T > liquidusTemperature
            else 50[W/(m*K)]
        }
        
        :>> calc specificHeat(T) {
            return 0.75[kJ/(kg*K)] when T > liquidusTemperature
            else 0.46[kJ/(kg*K)]
        }
        
        :>> calc density(T) {
            attribute T0 = 1600[°C];
            attribute rho0 = 7000[kg/m^3];
            return rho0 * (1 - thermalExpansion * (T - T0))
        }
    }
    
    // Chamber Thermal Field Evolution
    analysis def ChamberThermalField {
        doc /* 3D thermal field evolution in build chamber */
        
        subject chamber : BuildChamber;
        
        // Boundary conditions
        attribute wallTemp : TemperatureValue = 300[K];  // Cooled walls
        attribute heatedBedTemp : TemperatureValue[x,y];  // Spatially varying
        
        // Heat sources
        attribute dropletHeatSources : HeatSource[*] {
            attribute position : Position3D;
            attribute temperature : TemperatureValue;
            attribute heatOutput : PowerValue;
        }
        
        // Governing equation (heat diffusion)
        requirement heatDiffusion {
            doc /* ∂T/∂t = α∇²T + Q/ρc */
            attribute thermalDiffusivity = chamber.thermalConductivity / 
                                          (chamber.density * chamber.specificHeat);
        }
        
        // Temperature distribution
        calc temperatureField(x: LengthValue, y: LengthValue, z: LengthValue, t: TimeValue) 
            : TemperatureValue {
            
            // Simplified analytical solution for demonstration
            // Real implementation would use FEM/FDM
            attribute baseTemp = interpolate(heatedBedTemp, x, y) * exp(-z/characteristicLength);
            
            // Contribution from droplets
            attribute dropletContribution = sum over droplet in dropletHeatSources {
                droplet.heatOutput / (4 * π * chamber.thermalConductivity * 
                distance(position, droplet.position))
            };
            
            return baseTemp + dropletContribution;
        }
        
        // Constraint on chamber temperature
        constraint chamberTempLimit {
            doc /* Chamber walls must stay below 300°C per SR009 */
            all position in chamber.wallPositions {
                temperatureField(position, currentTime) < 300[°C]
            }
        }
    }
    
    // Cooling Rate Constraints and Predictions
    calc def CoolingRatePrediction {
        doc /* Predict cooling rate based on flight parameters */
        
        in initialTemp : TemperatureValue;
        in flightTime : DurationValue;
        in dropletSize : LengthValue;
        in material : MaterialProperties;
        
        // Use cooling model
        ref coolingModel : DropletCoolingModel {
            :>> dropletTemp = initialTemp;
            :>> dropletRadius = dropletSize / 2;
            :>> material = material;
            :>> gasVelocity = 0.5[m/s];  // Typical chamber convection
        }
        
        // Integrate cooling over flight time
        calc finalTemp : TemperatureValue {
            // Analytical approximation for exponential cooling
            attribute timeConstant = (material.density * dropletSize * material.specificHeat) / 
                                   (6 * coolingModel.convectionCoeff);
            return ambientTemp + (initialTemp - ambientTemp) * exp(-flightTime / timeConstant);
        }
        
        // Average cooling rate
        return avgCoolingRate : TemperatureRateValue = (initialTemp - finalTemp) / flightTime;
        
        // Verify requirement
        constraint meetsCoolingRequirement {
            avgCoolingRate > 1000[°C/s]  // SR010
        }
    }
    
    // Solidification Model
    analysis def SolidificationAnalysis {
        doc /* Phase change and microstructure evolution during solidification */
        
        in dropletState : DropletThermalState;
        in coolingRate : TemperatureRateValue;
        in material : MaterialProperties;
        
        // Solidification fraction
        calc solidFraction(T: TemperatureValue) : Real {
            when T > material.liquidusTemp { return 0 }
            when T < material.solidusTemp { return 1 }
            else { return (material.liquidusTemp - T) / 
                         (material.liquidusTemp - material.solidusTemp) }
        }
        
        // Latent heat release
        attribute latentHeatRelease = material.latentHeatFusion * 
                                     d(solidFraction)/dt * dropletState.mass;
        
        // Effective cooling rate during solidification
        attribute effectiveCoolingRate = coolingRate - latentHeatRelease / 
                                       (dropletState.mass * material.specificHeat);
        
        // Microstructure prediction
        calc grainSize : LengthValue {
            // Hall-Petch type relationship
            attribute A = 100[μm];  // Material constant
            attribute n = -0.5;     // Cooling rate exponent
            return A * (coolingRate / 1[K/s])^n;
        }
        
        // Quality metrics
        attribute microstructureUniformity = 1 - variance(grainSize) / mean(grainSize);
        
        constraint fineGrainStructure {
            doc /* Rapid solidification should produce fine grains */
            grainSize < 50[μm] when coolingRate > 1000[K/s]
        }
    }
    
    // Thermal Control Strategies
    action def ThermalControlStrategy {
        doc /* Active thermal management during deposition */
        
        in currentThermalField : TemperatureField;
        in targetBuildTemp : TemperatureValue;
        out heaterCommands : HeaterControl[*];
        out coolingCommands : CoolingControl;
        
        // Feedback control
        action measureField {
            :>> thermalCamera : OptrisPI1M;
            :>> measurement = thermalCamera.capture();
        }
        
        action computeError {
            :>> error = targetBuildTemp - currentThermalField.averageTemp;
            :>> gradient = currentThermalField.spatialGradient;
        }
        
        action generateControl {
            // PID control for heaters
            :>> proportional = Kp * error;
            :>> integral = Ki * integrate(error);
            :>> derivative = Kd * d(error)/dt;
            
            :>> heaterPower = proportional + integral + derivative;
            
            // Distribute power to maintain uniform field
            :>> heaterCommands = distributeHeaterPower(heaterPower, gradient);
        }
        
        // Cooling control for excessive temperatures
        if currentThermalField.maxTemp > safetyLimit {
            :>> coolingCommands.flowRate = maxFlowRate;
            :>> coolingCommands.zones = overheatedZones;
        }
    }
}