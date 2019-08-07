import React, { Component } from "react";
import axios from "axios";

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      test: '',
    };
  }
  getList = () => {
    axios
      .get("/api/polls/")
      .then(res => this.setState({test: JSON.stringify(res.data) }))
      .catch(err => console.log(err))
  };
  componentDidMount() {
    this.getList();
  }
  render() {
    return (
      <main className="content">
        <div className="jumbotron jumbotron-fluid">
          <div className="container">
            <h1 className="display-4">Fluid jumbotron</h1>
            <p className="lead">This is a modified jumbotron that occupies the entire horizontal space of its
              parent.</p>
          </div>
        </div>
        { this.state.test }
      </main>
    );
  }
}
export default App;