import { Products }       from "./components/Products";
import {
  BrowserRouter,
  Switch,
  Route
}                         from 'react-router-dom';
import { ProductsCreate } from "./components/ProductsCreate";
import { Orders }         from "./components/Orders";

function App() {
    return <BrowserRouter>
        <Switch>
            <Route path="/" element={<Products/>}/>
            <Route path="/create" element={<ProductsCreate/>}/>
            <Route path="/orders" element={<Orders/>}/>
        </Switch>
    </BrowserRouter>;
}

export default App;