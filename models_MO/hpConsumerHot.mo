within DHS.csBlocks;
model hpConsumerHot

  

    //////////////

    parameter Real eta=0.4;
    parameter Real etaEx=0.2;


    parameter Modelica.SIunits.Temperature Tin_cold=273+20 "K";
    parameter Modelica.SIunits.MassFlowRate mflow_in_cold=8 "kg/s";

    parameter Modelica.SIunits.MassFlowRate mflow_in_hot=8 "kg/s";

    parameter Modelica.SIunits.Temperature Tout_hot_target=273+50 "K";

    parameter Modelica.SIunits.Temperature Tout_hot_init=273+20 "K";

    Modelica.SIunits.Power Pelectric = hp.ht.ht.P;
    Modelica.SIunits.Power Pthermal_in = hp.ht.ht.Q2;
    Modelica.SIunits.Power Pthermal_out = hp.ht.ht.Q1;

    Modelica.SIunits.Power Pthermal_cons = 1E5 "W";

    Modelica.SIunits.Temperature Tout_cold = hp.ht.ht.staB2.T;
    Modelica.SIunits.Temperature Tout_hot = hp.ht.ht.staB1.T;
    Modelica.SIunits.Temperature Tin_hot = hp.ht.ht.staA1.T;


    Modelica.SIunits.Temperature Tin_cons=Tin_cons_internal; 
    Modelica.SIunits.Temperature Tout_cons = Tout_cons_internal;

    parameter Modelica.SIunits.Length length_pipes = 100 "m";
    parameter Modelica.SIunits.Length diameter_pipes = 0.2 "m";

protected

    Modelica.Blocks.Interfaces.RealInput Tin_cons_internal;
    Modelica.Blocks.Interfaces.RealInput Tout_cons_internal;

    parameter DHS.Types.ThermalDynamics thermalDynamicsIO = DHS.Types.ThermalDynamics.InitialOff;
    parameter DHS.Types.ThermalDynamics thermalDynamicsFIO = DHS.Types.ThermalDynamics.FixedInitialTout;

    package Medium1 = Buildings.Media.Water;
    package Medium2 = Buildings.Media.Water;

    ///////////////

    DHS.Subnetworks.hp_user hp(redeclare package Medium = Medium1, redeclare package MediumUser = Medium2,
            ht( redeclare DHS.HeatTransfer.Carnot_Tpi ht,
                hpMode = DHS.Types.HPmode.Heating, 
                thermalDynamics1= thermalDynamicsFIO,
                thermalDynamics2=thermalDynamicsIO,
                eta=eta,
                etaEx=etaEx,
                tau1=60,
                tau2=60,
                m1_flow_nominal=10,
                m2_flow_nominal=10,
                T1_start=Tout_hot_init
                ),
            consumer(heatIO(show_T=true, Q=Pthermal_cons, c=-1, m_flow_nominal=10, thermalDynamics=thermalDynamicsIO, tau=5)),
            pipesConsumer(pipeType = DHS.Types.PipeType.idealTransport , length=length_pipes, pipe_diameter=diameter_pipes ),
            pump(pump(m_flow=mflow_in_hot))
        );

 DHS.Subnetworks.BasicBlocks.source_sink interface ( redeclare package Medium = Medium1, 
        source(T=Tin_cold, m_flow=mflow_in_cold )
        );


    
Modelica.Blocks.Sources.Constant T_target( k=Tout_hot_target );

    
equation
    connect(interface.lport, hp.lport);

    connect(T_target.y, hp.ht.ht.Ttarget);

    connect(Tin_cons_internal, hp.consumer.heatIO.port_a_T);
    connect(Tout_cons_internal, hp.consumer.heatIO.port_b_T);

end hpConsumerHot;