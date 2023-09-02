mod flow;

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let zero = &String::from("0");
    let csi_index = args.get(1).unwrap_or(zero);

    let _csi = format!("csi{}", csi_index);
    //let c_out =

    // CStatusOut::get_bot_reply("bohumil", &csi);
}

// make the python interface
//
// cState will be written into the database as json upon every run
//
// check steps of dumb design
//      break into functions - plan
//      set up dumb design module
//      replicate + enhance cState
//      replicate + enhance python chunk of dumb design
//
// write a function that adds come_to_a_stop(coast) routine automatically to every_json
//                      (gonna have to figure out smart design first)
//
// ****
// inferring change of superstate based on whether
// how:
// adjacent state is present in current superstate
// if not present - look up superstates, where it is present -
// if multiple? - preferred the one closest to in order
// if none in order?
// ****
//

// fall back - generic fallback phrase + reiterate current latest initiative state
//
