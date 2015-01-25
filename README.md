# bpe_capstone

JSON Query Object:

{ 
	"query": {
		"query_id": 	"number"
		"start": 		"ISO8601 timestamp"
		"end":			"ISO8601 timestamp"
		"stations": 	["strings"]		
		"attributes":	
		{ [
					"voltage": {
						["B", "L", "D", "A", "T", "G"],			<- measurement
						["A", "M", "R", "I", "F", "RF"], 		<- phasors
						["VP", "VZ", "VN", "VA", "VB", "VC"], 	<- type
						[">", ">=", "<", "<=", "==", "!="], 	<- condition
						["numbers"]								<- constraint
					}
					"current": {
						["B", "L", "D", "A", "T", "G"],
						["A", "M", "R", "I", "F", "RF"], 
						["IP", "IZ", "IN", "IA", "IB", "IC"], 
						[">", ">=", "<", "<=", "==", "!="], 
						["numbers"]
					}
					"freq": {
						["B", "L", "D", "A", "T", "G"],
						["A", "M", "R", "I", "F", "RF"], 
						["F", "R"], 
						[">", ">=", "<", "<=", "==", "!="], 
						["numbers"]
					}
					"nomvolts": "number"
		] }
	}
	"analysis": {
		"file": 	"string"
		"type": 	"string"
	}
	"user": {
		"name": 	"string"
		"pw": 		"string"
		"required": true
	}
}

