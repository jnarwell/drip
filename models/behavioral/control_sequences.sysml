package ControlSequences {
    import ScalarValues::*;
    import ISQ::*;
    import SI::*;
    import DropletControlBehavior::*;
    
    // Thermal Predictive Control Loop Sequence
    interaction def ThermalPredictiveControlLoop {
        doc /* 
         * Main control sequence showing component interactions
         * Camera → STM32 → FPGA → Transducers
         */
        
        // Participants
        :>> participant camera : OptrisPI1M;
        :>> participant stm32 : STM32Controller;
        :>> participant fpga : CycloneIVFPGA;
        :>> participant amplifiers : SixChannelAmplifier[4];
        :>> participant transducers : UltrasonicTransducer[24];
        :>> participant droplet : Droplet;
        
        // Main control sequence
        message captureThermal from camera to stm32 {
            :>> payload thermalFrame : ThermalImageData;
            :>> latency = 31.25[ms];  // 32Hz frame rate
        }
        
        message extractDropletState from stm32 to stm32 {
            :>> duration = 0.5[ms];  // Image processing time
        }
        
        message calculateTrajectory from stm32 to stm32 {
            :>> duration = 0.4[ms];  // Trajectory computation
        }
        
        message sendPhaseUpdate from stm32 to fpga {
            :>> payload phaseData : PhaseArrayConfig;
            :>> protocol = "SPI";
            :>> dataRate = 50[MHz];
            :>> latency = 0.02[ms];
        }
        
        message distributePhases from fpga to amplifiers {
            :>> payload individualPhases : PhaseValue[6];
            :>> latency = 0.01[ms];
            :>> parallel = true;  // All amplifiers updated simultaneously
        }
        
        message driveTransducers from amplifiers to transducers {
            :>> payload driveSignal : SinusoidalSignal;
            :>> frequency = 40[kHz];
            :>> latency = 0.001[ms];
        }
        
        message applyForce from transducers to droplet {
            :>> payload acousticForce : ForceVector;
            :>> responseTime = 0.2[ms];  // Droplet response time
        }
        
        // Total loop constraint
        constraint totalLoopTime {
            sum(all message latencies) < 3[ms]  // SR014 requirement
        }
    }
    
    // Material Transition Sequence
    interaction def MaterialTransitionSequence {
        doc /* Protocol for switching between Aluminum and Steel materials */
        
        :>> participant controller : SystemController;
        :>> participant crucible : HeatedCrucible;
        :>> participant inductionHeater : InductionHeatingSystem;
        :>> participant coolingSystem : ActiveCooling;
        :>> participant acousticArray : TransducerArray;
        
        // Aluminum to Steel transition
        alt aluminumToSteel {
            message initiateTransition from controller to crucible {
                :>> command = "PrepareForSteel";
            }
            
            message stopAlFlow from crucible to crucible {
                :>> action = "CloseAluminumValves";
                :>> duration = 0.5[s];
            }
            
            message enableInduction from controller to inductionHeater {
                :>> power = 3[kW];
                :>> targetTemp = 1580[°C];
            }
            
            message rampTemperature from inductionHeater to crucible {
                :>> rampRate = 50[°C/s];
                :>> duration = 18[s];  // (1580-700)/50
            }
            
            message adjustCooling from controller to coolingSystem {
                :>> flowRate = 10[L/min];  // Increased for steel
            }
            
            message reconfigureAcoustic from controller to acousticArray {
                :>> power = 360[W];  // Double power for steel
                :>> phaseCompensation = "SteelViscosity";
            }
            
            message confirmReady from crucible to controller {
                :>> status = "SteelModeReady";
                :>> actualTemp = 1580[°C];
            }
            
            message startSteelFlow from controller to crucible {
                :>> command = "OpenSteelValves";
            }
        }
        
        // Steel to Aluminum transition
        alt steelToAluminum {
            message initiateTransition from controller to crucible {
                :>> command = "PrepareForAluminum";
            }
            
            message stopSteelFlow from crucible to crucible {
                :>> action = "CloseSteelValves";
            }
            
            message disableInduction from controller to inductionHeater {
                :>> power = 0[W];
            }
            
            message activeCool from controller to coolingSystem {
                :>> flowRate = 20[L/min];  // Max cooling
                :>> duration = 25[s];  // Cool from 1580 to 700°C
            }
            
            message monitorCooling from crucible to controller {
                :>> loop {
                    :>> tempReading : TemperatureValue;
                    :>> interval = 1[s];
                    :>> until tempReading <= 750[°C];
                }
            }
            
            message reduceAcoustic from controller to acousticArray {
                :>> power = 180[W];
                :>> phaseCompensation = "AluminumViscosity";
            }
            
            message startAlFlow from controller to crucible {
                :>> command = "OpenAluminumValves";
            }
        }
    }
    
    // Multi-droplet Coordination Sequence
    interaction def MultiDropletCoordination {
        doc /* Coordination of multiple droplets in flight */
        
        :>> participant coordinator : DropletCoordinator;
        :>> participant tracker : DropletTracker;
        :>> participant phaseController : PhaseArrayController;
        :>> participant droplets : Droplet[1..*];
        
        // Tracking loop
        loop trackingCycle {
            :>> rate = 1[kHz];  // 1ms cycle
            
            message scanField from coordinator to tracker {
                :>> region = "ActiveBuildZone";
            }
            
            message reportPositions from tracker to coordinator {
                :>> dropletStates : DropletState[*];
                :>> timestamp : TimeValue;
            }
            
            message calculateInterference from coordinator to coordinator {
                :>> action = "ComputeMutualForces";
                :>> complexity = O(n²);  // n = number of droplets
            }
            
            message optimizePhases from coordinator to phaseController {
                :>> objective = "MinimizeInterference";
                :>> constraints = "MaintainTrajectories";
            }
            
            ref sequence : ThermalPredictiveControlLoop {
                :>> parallel = true;  // Run for each droplet
            }
        }
        
        // Collision avoidance
        alt collisionDetected {
            message predictCollision from tracker to coordinator {
                :>> dropletPair : Droplet[2];
                :>> timeToCollision : DurationValue;
            }
            
            when timeToCollision < 50[ms] {
                message emergencyRedirect from coordinator to phaseController {
                    :>> priority = "Critical";
                    :>> action = "SeparateDroplets";
                }
            }
            
            else when timeToCollision < 200[ms] {
                message adjustTrajectory from coordinator to phaseController {
                    :>> priority = "High";
                    :>> action = "ModifyPaths";
                }
            }
        }
    }
    
    // Emergency Shutdown Sequence
    interaction def EmergencyShutdownSequence {
        doc /* Critical safety shutdown procedure */
        
        :>> participant emergencyStop : EmergencyStopButton;
        :>> participant safetyController : SafetyPLC;
        :>> participant powerSystem : PowerDistribution;
        :>> participant acousticSystem : AcousticSubsystem;
        :>> participant thermalSystem : ThermalSubsystem;
        :>> participant ventilation : ExhaustSystem;
        
        // Immediate actions (< 10ms)
        message eStopPressed from emergencyStop to safetyController {
            :>> latency < 1[ms];
            :>> priority = "Maximum";
        }
        
        par {  // Parallel immediate actions
            message cutAcousticPower from safetyController to acousticSystem {
                :>> action = "DisableAllAmplifiers";
                :>> latency < 5[ms];
            }
            
            message cutThermalPower from safetyController to thermalSystem {
                :>> action = "DisableAllHeaters";
                :>> latency < 5[ms];
            }
            
            message activateVent from safetyController to ventilation {
                :>> action = "MaximumExhaust";
                :>> latency < 10[ms];
            }
        }
        
        // Secondary actions (< 100ms)
        message saveDropletStates from acousticSystem to safetyController {
            :>> data = "LastKnownPositions";
            :>> purpose = "PreventDebrisGeneration";
        }
        
        message enableGravityCapture from safetyController to acousticSystem {
            :>> action = "ActivateCatchBasin";
            :>> duration = 2[s];  // Allow droplets to fall safely
        }
        
        // Tertiary actions (< 1s)
        message activateCooling from safetyController to thermalSystem {
            :>> coolingMode = "Emergency";
            :>> flowRate = "Maximum";
        }
        
        message logShutdown from safetyController to safetyController {
            :>> timestamp : TimeValue;
            :>> cause : String;
            :>> systemState : SystemSnapshot;
        }
        
        // Confirmation
        message confirmSafeState from safetyController to emergencyStop {
            :>> allSystemsSafe : Boolean;
            :>> canRestart : Boolean;
        }
    }
    
    // Startup Sequence
    interaction def SystemStartupSequence {
        doc /* Controlled startup procedure with safety checks */
        
        :>> participant operator : HumanOperator;
        :>> participant hmi : HMIInterface;
        :>> participant controller : MainController;
        :>> participant subsystems : Subsystem[*];
        
        message initiateStartup from operator to hmi {
            :>> command = "SystemStart";
        }
        
        loop initializationLoop for subsystem in subsystems {
            message checkSubsystem from controller to subsystem {
                :>> test = "SelfDiagnostic";
            }
            
            alt diagnosticResult {
                opt passed {
                    message reportReady from subsystem to controller {
                        :>> status = "Operational";
                    }
                }
                
                opt failed {
                    message reportFault from subsystem to controller {
                        :>> status = "Fault";
                        :>> details : FaultInfo;
                    }
                    
                    message abortStartup from controller to hmi {
                        :>> reason = "SubsystemFailure";
                    }
                    
                    break;  // Exit startup
                }
            }
        }
        
        message enableOperation from controller to subsystems {
            :>> mode = "Operational";
            :>> parallel = true;
        }
        
        message confirmStartup from controller to hmi {
            :>> systemReady = true;
        }
    }
}