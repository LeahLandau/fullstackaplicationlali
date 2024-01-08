import React, { useContext, useEffect, useState } from 'react';

import 'devextreme/dist/css/dx.light.css';
import TreeView from 'devextreme-react/tree-view';

import ImgContext from '../context/ImageReduction';
// import axios from 'axios';

const SelectionImage = () => {

    const { setImagePath } = useContext(ImgContext)
    const [selectedNode, setSelectedNode] = useState({});
    const [data, setData] = useState([])

    const createObject = (arr, num, val = '') => {

        const arrSplit = arr.map((item) => {
            const element = item.split("/").slice(num + 1)
            return element[0]
        })
        const arrWithoutMulti = arrSplit.filter((value, index) => arrSplit.indexOf(value) === index)

        return arrWithoutMulti.map((item) => {
            const path = val + '/' + item;
            const pathStart = path.startsWith('/') ? path : '/' + path;
            const arrFiltered = arr.filter((element) => element.startsWith(pathStart));
            return (item.endsWith(".jpeg")) || (item.endsWith(".jp2")) ? { name: item, path: path, isFolder: false } :
                { name: item, path: path, isFolder: true, items: createObject(arrFiltered, num + 1, path) };
        });
    }
    // only now:
    const example = [ '/server/relax.jp2','/server/img1/s.jp2', '/server/img1/jhgf.B1.jp2',
        '/server/img3/gfd.B1.jp2', '/src/img4/jhgttf.B1.jp2', '/server/img.B1.jp2']

    const hierarchicalData = createObject(example, 0)


    useEffect(() => {
        // when lea make it:
        // const path_name = "?lea_need_decided?";
        // const response = axios.get('http://localhost:5000/??lea_need_create_endpoint??', path_name);
        // const hierarchical = response.data;
        // const correctObject = createObject(hierarchical, 0);
        // setData(correctObject);

        // only now:
        setData(hierarchicalData)
    }, [])

    const selectItem = (e) => {
        const clickedNode = e.itemData;
        const updateNode = (node, nodeName) => {
            if (node.name === nodeName) {
                return { ...node, expanded: !node.expanded };
            }
            if (node.items && node.items.length > 0) {
                const updatedItems = node.items.map((item) => {
                    return updateNode(item, nodeName);
                });
                return { ...node, items: updatedItems, };
            }
            return node;
        };
        const updatedData = data.map((node) => updateNode(node, clickedNode.name));
        setData(updatedData);

        if (!clickedNode.isFolder) {
            setSelectedNode(clickedNode);
            // just to run now:
            // setImagePath("/share/vistorage/ofakim-test/OC2_0016483137/OC2_0016483137.B1.jp2" )
            setImagePath('/server/relax.jp2')
        }
    };

    return <>
        <TreeView
            keyExpr="name"
            displayExpr="name"
            dataSource={data}
            searchEnabled={true}
            selectionMode="single"
            selectByClick={true}
            onItemSelectionChanged={selectItem}
        />
        <h1>
            {
                (selectedNode.path !== undefined) ? `the path is : ${selectedNode.path}` : ''
            }
        </h1>
    </>

}

export default SelectionImage;