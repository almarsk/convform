mod flow;
use flow::Flow;
use std::fs::read_to_string;

fn main() {
    let flow_path = "bots/bohumil.json";
    let flow_file = read_to_string(flow_path).unwrap();

    match Flow::validate_behavior(flow_path, &flow_file) {
        Err(e) => {
            println!("validation error: {:?}", e);
        }
        Ok(flow) => println!("{:?}", flow),
    }
}

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
