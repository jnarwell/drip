package SystemStates {
    import ScalarValues::*;
    import ISQ::*;
    import SI::*;
    
    // Top-level System States
    state def DRIPSystemStates {
        doc /* Main operational states of the DRIP acoustic manufacturing system */
        
        entry state off;
        state initialization;
        state operational;
        state error;
        
        transition off_to_init
            first off
            accept powerOnCommand
            then initialization;
            
        transition init_to_operational
            first initialization
            accept checksPass
            then operational;
            
        transition init_to_error
            first initialization
            accept checksFail
            then error;
            
        transition operational_to_error
            first operational
            accept faultDetected
            then error;
            
        transition error_to_off
            first error
            accept emergencyStop
            then off;
            
        transition error_recovery
            first error
            accept recoveryComplete
            then operational.idle;
    }
    
    // Operational Substates
    state def OperationalStates {
        doc /* Substates within the operational mode */
        
        entry state idle;
        state preheating;
        state building;
        state cooling;
        
        transition idle_to_preheat
            first idle
            accept startBuildCommand
            then preheating;
            
        transition preheat_to_building
            first preheating
            accept targetTempReached
            guard { crucibleTemp >= targetTemp - 5[K] }
            then building;
            
        transition building_to_cooling
            first building
            accept buildComplete
            then cooling;
            
        transition cooling_to_idle
            first cooling
            accept safeTempReached
            guard { maxTemp < 50[°C] }
            then idle;
            
        // Error transitions
        transition any_to_error
            accept criticalFault
            then error;
    }
    
    // Material-specific Building States
    state def BuildingStates {
        doc /* Material-specific operational modes during building */
        
        entry state selectMaterial;
        state aluminumMode;
        state steelMode;
        state multiMaterialMode;
        
        // Aluminum building parameters
        state aluminumMode {
            entry action {
                setCrucibleTemp(700[°C]);
                setAcousticPower(180[W]);
                setCoolingFlow(5[L/min]);
            }
            
            invariant aluminumTempRange {
                crucibleTemp >= 690[°C] and crucibleTemp <= 750[°C]
            }
        }
        
        // Steel building parameters
        state steelMode {
            entry action {
                setCrucibleTemp(1580[°C]);
                setAcousticPower(360[W]);
                setCoolingFlow(10[L/min]);
                enableInductionHeating();
            }
            
            invariant steelTempRange {
                crucibleTemp >= 1550[°C] and crucibleTemp <= 1650[°C]
            }
        }
        
        // Multi-material transitions
        state multiMaterialMode {
            state depositingAluminum : aluminumMode;
            state transitioning;
            state depositingSteel : steelMode;
            
            transition al_to_transition
                first depositingAluminum
                accept materialSwitchCommand
                then transitioning;
                
            transition transition_to_steel
                first transitioning
                accept transitionComplete
                guard { crucibleTemp >= 1550[°C] }
                then depositingSteel;
                
            transition steel_to_transition
                first depositingSteel
                accept materialSwitchCommand
                then transitioning;
                
            transition transition_to_al
                first transitioning
                accept transitionComplete
                guard { crucibleTemp <= 750[°C] }
                then depositingAluminum;
        }
    }
    
    // Individual Droplet Lifecycle
    state def DropletLifecycle {
        doc /* State progression for individual droplets from generation to solidification */
        
        entry state generated;
        state levitated;
        state inTransit;
        state depositing;
        state solidified;
        final state incorporated;
        
        // State transitions with timing constraints
        transition generation
            first generated
            accept exitMeltPool
            then levitated
            effect { startTime = now(); }
            
        transition engagement
            first levitated
            accept acousticFieldEngaged
            guard { acousticPressure > minLevitationPressure }
            then inTransit
            effect { engagementTime = now() - startTime; }
            
        transition trajectory
            first inTransit
            accept reachedTargetZone
            guard { distanceToTarget < 1[mm] }
            then depositing
            effect { 
                flightTime = now() - engagementTime;
                assert { flightTime < 200[ms] }  // Max flight time
            }
            
        transition deposition
            first depositing
            accept touchedSurface
            then solidified
            effect {
                releaseAcousticField();
                startCoolingTimer();
            }
            
        transition solidification
            first solidified
            accept coolingComplete
            guard { temperature < solidusTemp }
            then incorporated
            effect {
                coolingTime = now() - coolingStartTime;
                coolingRate = (meltTemp - temperature) / coolingTime;
                assert { coolingRate > 1000[°C/s] }  // SR010
            }
    }
    
    // Error States with Recovery Actions
    state def ErrorStates {
        doc /* System error states and recovery procedures */
        
        entry state errorDetection;
        state thermalRunaway;
        state acousticFailure;
        state materialBlockage;
        state powerFailure;
        state communicationLoss;
        
        // Thermal runaway handling
        state thermalRunaway {
            entry action {
                disableAllHeaters();
                maximizeCoolingFlow();
                activateEmergencyVent();
                alertOperator("THERMAL RUNAWAY DETECTED");
            }
            
            invariant maxTempExceeded {
                anyComponentTemp > maxSafeTemp
            }
            
            exit action {
                logIncident();
                requireMaintenanceCheck();
            }
        }
        
        // Acoustic system failure
        state acousticFailure {
            entry action {
                pauseMaterialFeed();
                maintainExistingField();
                diagnosticScan();
            }
            
            state transducerFailure {
                entry action identifyFailedTransducer();
                exit action reconfigureArray();
            }
            
            state amplifierFailure {
                entry action switchToBackupAmplifier();
            }
            
            state phaseDesync {
                entry action recalibratePhaseArray();
            }
        }
        
        // Material feed blockage
        state materialBlockage {
            entry action {
                stopFeedMotor();
                reverseFeeder(2[s]);
                attemptClear();
            }
            
            state partialBlockage {
                entry action reduceFlowRate(50%);
            }
            
            state completeBlockage {
                entry action {
                    shutdownFeed();
                    requireManualIntervention();
                }
            }
        }
        
        // Recovery procedures
        action def RecoveryProcedure {
            in errorType : ErrorType;
            out recoverySuccess : Boolean;
            
            action diagnose : DiagnoseError {
                in error = errorType;
                out rootCause : String;
                out severity : Integer;
            }
            
            action attemptAutoRecovery : AutoRecovery {
                in cause = diagnose.rootCause;
                out success : Boolean;
            }
            
            action manualIntervention : RequestOperator {
                in severity = diagnose.severity;
                out operatorAction : String;
            }
            
            first diagnose;
            
            if attemptAutoRecovery.success {
                recoverySuccess = true;
            } else {
                then manualIntervention;
                recoverySuccess = false;
            }
        }
    }
}