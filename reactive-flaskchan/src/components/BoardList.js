export default function BoardList(){
  return (
      <div className="boardList">
          <div className="listContent">
              <div className="homeBtn">
                  <a href="/">/~</a>
              </div>
              <div className="stripBoard">/b/</div>
              <div className="stripBoard">/soc/</div>
              <div className="stripBoard">/pol/</div>
              <a id="addBoardToList"><i data-feather="plus-circle"></i></a>
          </div>
          <div className="maintenanceList">
              <a><i data-feather="eye"></i></a>
              <a id="settingButton" href="#settings"><i data-feather="settings"></i></a>
          </div>
      </div>
  );
}